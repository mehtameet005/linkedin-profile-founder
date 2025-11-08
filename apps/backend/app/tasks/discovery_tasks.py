"""
Background tasks for the discovery pipeline
"""
import asyncio
from celery import chain
from sqlalchemy import select
from app.core.celery_app import celery_app
from app.db.session import AsyncSessionLocal
from app.models.job import Job, JobStatus
from app.models.icp import ICP
from app.models.persona import Persona
from app.models.candidate import Candidate
from app.services.crawler import crawler_service
from app.services.nlp import nlp_service
from app.services.icp_generator import icp_generator_service
from app.services.discovery import discovery_service
from app.services.scoring import scoring_service
import logging

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="process_job_pipeline")
def process_job_pipeline(self, job_id: str):
    """
    Main pipeline task that orchestrates the entire discovery process

    Args:
        job_id: The job ID to process
    """
    # Chain the tasks together
    workflow = chain(
        crawl_website_task.s(job_id),
        generate_icp_task.s(job_id),
        run_discovery_task.s(job_id),
    )

    return workflow.apply_async()


@celery_app.task(bind=True, name="crawl_website_task")
def crawl_website_task(self, job_id: str):
    """Crawl the website and analyze content"""

    async def _crawl():
        async with AsyncSessionLocal() as db:
            # Get job
            result = await db.execute(select(Job).where(Job.id == job_id))
            job = result.scalar_one_or_none()

            if not job:
                raise ValueError(f"Job {job_id} not found")

            # Update status
            job.status = JobStatus.PROCESSING
            await db.commit()

            try:
                # Crawl website
                logger.info(f"Crawling website: {job.website_url}")
                crawl_data = await crawler_service.crawl_website(job.website_url)

                # Analyze content
                logger.info(f"Analyzing content for job {job_id}")
                analysis = await nlp_service.analyze_website_content(crawl_data)

                return {"analysis": analysis, "crawl_data": crawl_data}

            except Exception as e:
                job.status = JobStatus.FAILED
                await db.commit()
                logger.error(f"Error in crawl task for job {job_id}: {str(e)}")
                raise

    return asyncio.run(_crawl())


@celery_app.task(bind=True, name="generate_icp_task")
def generate_icp_task(self, crawl_result: dict, job_id: str):
    """Generate ICP and personas from website analysis"""

    async def _generate():
        async with AsyncSessionLocal() as db:
            # Get job
            result = await db.execute(select(Job).where(Job.id == job_id))
            job = result.scalar_one_or_none()

            if not job:
                raise ValueError(f"Job {job_id} not found")

            try:
                # Generate ICP
                logger.info(f"Generating ICP for job {job_id}")
                icp_data = await icp_generator_service.generate_icp(
                    crawl_result["analysis"], job.website_url
                )

                # Create ICP record
                icp = ICP(job_id=job_id, **icp_data)
                db.add(icp)
                await db.flush()

                # Generate personas
                logger.info(f"Generating personas for ICP {icp.id}")
                personas_data = await icp_generator_service.generate_personas(icp_data)

                # Create persona records
                for persona_data in personas_data:
                    persona = Persona(icp_id=icp.id, **persona_data)
                    db.add(persona)

                await db.commit()
                await db.refresh(icp)

                return {"icp_id": icp.id}

            except Exception as e:
                job.status = JobStatus.FAILED
                await db.commit()
                logger.error(f"Error in ICP generation for job {job_id}: {str(e)}")
                raise

    return asyncio.run(_generate())


@celery_app.task(bind=True, name="run_discovery_task")
def run_discovery_task(self, icp_result: dict, job_id: str):
    """Run the discovery process to find LinkedIn profiles"""

    async def _discover():
        async with AsyncSessionLocal() as db:
            # Get job and ICP
            result = await db.execute(select(Job).where(Job.id == job_id))
            job = result.scalar_one_or_none()

            if not job:
                raise ValueError(f"Job {job_id} not found")

            icp_id = icp_result["icp_id"]
            result = await db.execute(select(ICP).where(ICP.id == icp_id))
            icp = result.scalar_one_or_none()

            if not icp:
                raise ValueError(f"ICP {icp_id} not found")

            # Get personas
            result = await db.execute(select(Persona).where(Persona.icp_id == icp_id))
            personas = result.scalars().all()

            try:
                all_candidates = []

                # Search for profiles for each persona
                for persona in personas:
                    logger.info(f"Running discovery for persona: {persona.persona_name}")

                    # Convert persona to dict
                    persona_dict = {
                        "titles": persona.titles,
                        "keywords": persona.keywords,
                        "goals": persona.goals,
                    }

                    # Search profiles
                    profiles = await discovery_service.search_profiles(
                        persona_dict, limit=20
                    )

                    # Parse and score each profile
                    for profile_data in profiles:
                        parsed = discovery_service.parse_profile_snippet(profile_data)

                        # Score the candidate
                        icp_dict = {
                            "industry": icp.industry,
                            "sub_industries": icp.sub_industries,
                        }

                        score_data = scoring_service.score_candidate(
                            parsed, persona_dict, icp_dict
                        )

                        # Create candidate record
                        candidate = Candidate(
                            job_id=job_id,
                            linkedin_url=parsed["linkedin_url"],
                            inferred_name=parsed.get("inferred_name"),
                            inferred_title=parsed.get("inferred_title"),
                            inferred_location=parsed.get("inferred_location"),
                            inferred_company=parsed.get("inferred_company"),
                            result_snippet=parsed["result_snippet"],
                            scores=score_data["scores"],
                            explainability=score_data["explainability"],
                        )

                        all_candidates.append(candidate)

                # Bulk insert candidates
                if all_candidates:
                    db.add_all(all_candidates)

                # Mark job as completed
                job.status = JobStatus.COMPLETED
                await db.commit()

                logger.info(
                    f"Discovery completed for job {job_id}. Found {len(all_candidates)} candidates."
                )

                return {"candidates_found": len(all_candidates)}

            except Exception as e:
                job.status = JobStatus.FAILED
                await db.commit()
                logger.error(f"Error in discovery for job {job_id}: {str(e)}")
                raise

    return asyncio.run(_discover())
