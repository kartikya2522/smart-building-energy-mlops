'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

interface InsightsData {
  top_drivers: string[];
  descriptions: string[];
}

export default function Insights() {
  const [insights, setInsights] = useState<InsightsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchInsights = async () => {
      try {
        const response = await fetch('http://localhost:8000/insights');
        if (!response.ok) {
          throw new Error('Failed to fetch insights');
        }
        const data: InsightsData = await response.json();
        setInsights(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchInsights();
  }, []);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.6 },
    },
  };

  return (
    <main className="bg-black min-h-screen px-4 py-16">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-12"
        >
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-4">
            Key Drivers
          </h1>
          <p className="text-xl text-gray-400 max-w-2xl">
            Understand which environmental factors most influence your building's energy consumption based on model analysis.
          </p>
        </motion.div>

        {/* Loading State */}
        {loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center justify-center py-20"
          >
            <div className="text-center">
              <div className="animate-pulse mb-4">
                <div className="h-12 w-12 bg-gray-700 rounded-full mx-auto"></div>
              </div>
              <p className="text-gray-400">Loading insights...</p>
            </div>
          </motion.div>
        )}

        {/* Error State */}
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-red-900/30 border border-red-700 text-red-300 px-6 py-4 mb-8"
          >
            {error}
          </motion.div>
        )}

        {/* Insights List */}
        {insights && !loading && (
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="space-y-6"
          >
            {insights.top_drivers.map((driver, index) => (
              <motion.div
                key={index}
                variants={itemVariants}
                className="border border-gray-700 p-8 bg-black hover:border-green-500/30 transition-colors"
              >
                {/* Driver Name and Rank */}
                <div className="flex items-start gap-6">
                  <div className="flex-shrink-0 w-12 h-12 bg-green-500 text-black rounded-full flex items-center justify-center font-bold text-lg">
                    {index + 1}
                  </div>
                  <div className="flex-grow">
                    <h2 className="text-2xl font-semibold text-green-400 mb-3">
                      {driver}
                    </h2>
                    <p className="text-gray-300 leading-relaxed text-lg">
                      {insights.descriptions[index]}
                    </p>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        )}

        {/* Empty State */}
        {!loading && !insights && !error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="border border-dashed border-gray-700 p-12 text-center"
          >
            <p className="text-gray-500">No insights available</p>
          </motion.div>
        )}

        {/* Summary Section */}
        {insights && !loading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
            className="mt-16 border border-gray-700 p-8 bg-black"
          >
            <h3 className="text-2xl font-semibold text-white mb-4">
              How to Use These Insights
            </h3>
            <p className="text-gray-300 leading-relaxed">
              These key drivers represent the environmental factors that most significantly impact your building's energy consumption patterns. By monitoring and optimizing these variables through operational adjustments or infrastructure improvements, you can effectively reduce overall energy consumption and associated costs.
            </p>
          </motion.div>
        )}
      </div>
    </main>
  );
}
