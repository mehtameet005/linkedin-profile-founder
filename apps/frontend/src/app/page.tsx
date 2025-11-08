import Link from 'next/link';
import { ArrowRight, Target, Users, Search, BarChart } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Target className="h-8 w-8 text-blue-600" />
            <h1 className="text-2xl font-bold text-gray-900">ProfileFinder AI</h1>
          </div>
          <nav className="flex gap-4">
            <Link
              href="/login"
              className="px-4 py-2 text-gray-700 hover:text-gray-900 transition"
            >
              Login
            </Link>
            <Link
              href="/signup"
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              Get Started
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h2 className="text-5xl font-bold text-gray-900 mb-6">
          Find Your Ideal Customers
          <br />
          <span className="text-blue-600">Powered by AI</span>
        </h2>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Enter any business website and instantly generate precise buyer personas, ideal
          customer profiles, and discover qualified LinkedIn prospects.
        </p>
        <Link
          href="/dashboard"
          className="inline-flex items-center gap-2 px-8 py-4 bg-blue-600 text-white text-lg rounded-lg hover:bg-blue-700 transition shadow-lg"
        >
          Start Discovery
          <ArrowRight className="h-5 w-5" />
        </Link>
      </section>

      {/* Features */}
      <section className="container mx-auto px-4 py-20">
        <h3 className="text-3xl font-bold text-center mb-12">How It Works</h3>
        <div className="grid md:grid-cols-4 gap-8">
          <FeatureCard
            icon={<Target className="h-10 w-10 text-blue-600" />}
            title="Website Analysis"
            description="AI crawls and understands any business website to extract key insights"
          />
          <FeatureCard
            icon={<Users className="h-10 w-10 text-purple-600" />}
            title="ICP Generation"
            description="Automatically generates ideal customer profiles and buyer personas"
          />
          <FeatureCard
            icon={<Search className="h-10 w-10 text-green-600" />}
            title="Profile Discovery"
            description="Finds relevant LinkedIn profiles using legal search APIs"
          />
          <FeatureCard
            icon={<BarChart className="h-10 w-10 text-orange-600" />}
            title="Smart Scoring"
            description="Ranks prospects with AI-powered relevance scoring and explanations"
          />
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h3 className="text-4xl font-bold mb-6">Ready to Find Your Ideal Customers?</h3>
          <p className="text-xl mb-8 opacity-90">
            Start discovering qualified prospects in minutes
          </p>
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 px-8 py-4 bg-white text-blue-600 text-lg rounded-lg hover:bg-gray-100 transition shadow-lg"
          >
            Get Started Free
            <ArrowRight className="h-5 w-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8">
        <div className="container mx-auto px-4 text-center text-gray-600">
          <p>&copy; 2024 ProfileFinder AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="p-6 bg-white rounded-xl shadow-sm border hover:shadow-md transition">
      <div className="mb-4">{icon}</div>
      <h4 className="text-xl font-semibold mb-2">{title}</h4>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}
