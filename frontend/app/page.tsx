'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import HeroEarth from '../components/HeroEarth';

export default function Home() {
  const fadeInUp = {
    initial: { opacity: 0, y: 20 },
    whileInView: { opacity: 1, y: 0 },
    viewport: { once: true },
    transition: { duration: 0.6 },
  };

  const staggerContainer = {
    initial: { opacity: 0 },
    whileInView: { opacity: 1 },
    viewport: { once: true },
  };

  const staggerItem = {
    initial: { opacity: 0, y: 20 },
    whileInView: { opacity: 1, y: 0 },
    transition: { duration: 0.5 },
  };

  return (
    <>
      {/* Hero Section */}
      <section className="min-h-screen bg-black flex items-center justify-center px-4 relative overflow-hidden">
        {/* Animated Background */}
        {/* Cinematic 3D Background */}
        <HeroEarth />

        {/* Content - positioned relative to sit above background */}
        <div className="max-w-4xl w-full relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
              Energy clarity for buildings that <span className="text-green-400">matter</span>
            </h1>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <p className="text-xl md:text-2xl text-gray-400 mb-8 max-w-2xl leading-relaxed">
              Predict energy consumption with precision. Understand building performance. Make informed decisions.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <Link
              href="/predict"
              className="inline-block bg-white text-black px-8 py-3 font-medium hover:bg-gray-200 transition-colors"
            >
              Start Predicting
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="bg-black px-4 py-20">
        <div className="max-w-4xl mx-auto">
          <motion.div {...fadeInUp}>
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-8">The Problem</h2>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
            <p className="text-xl text-gray-300 leading-relaxed max-w-2xl">
              Buildings account for nearly 40% of global energy consumption. Yet most lack real-time visibility into their energy patterns. This blindness costs money, wastes resources, and prevents meaningful <span className="text-green-400">climate action</span>.
            </p>
          </motion.div>
        </div>
      </section>

      {/* What We Do Section */}
      <section className="bg-black px-4 py-20">
        <div className="max-w-4xl mx-auto">
          <motion.div {...fadeInUp}>
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-16">What This Platform Does</h2>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="whileInView"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8"
          >
            {/* Item 1 */}
            <motion.div variants={staggerItem} className="border border-gray-700 p-8 hover:border-blue-500/30 transition-colors">
              <h3 className="text-xl font-semibold text-white mb-4"><span className="text-blue-400">Predict</span> Consumption</h3>
              <p className="text-gray-400 leading-relaxed">
                Forecast energy demand hours and days ahead with machine learning trained on real building data.
              </p>
            </motion.div>

            {/* Item 2 */}
            <motion.div variants={staggerItem} className="border border-gray-700 p-8 hover:border-blue-500/30 transition-colors">
              <h3 className="text-xl font-semibold text-white mb-4"><span className="text-blue-400">Identify</span> Patterns</h3>
              <p className="text-gray-400 leading-relaxed">
                Uncover hidden inefficiencies and behavioral patterns that drive your building's energy signature.
              </p>
            </motion.div>

            {/* Item 3 */}
            <motion.div variants={staggerItem} className="border border-gray-700 p-8 hover:border-green-500/30 transition-colors">
              <h3 className="text-xl font-semibold text-white mb-4"><span className="text-green-400">Quantify</span> Impact</h3>
              <p className="text-gray-400 leading-relaxed">
                Measure the real-world impact of efficiency improvements in energy saved and emissions reduced.
              </p>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="bg-black px-4 py-20">
        <div className="max-w-4xl mx-auto">
          <motion.div {...fadeInUp}>
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-16">How It Works</h2>
          </motion.div>

          <div className="space-y-8">
            {/* Step 1 */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5 }}
              className="flex gap-6 items-start"
            >
              <div className="flex-shrink-0 w-12 h-12 bg-white text-black rounded-full flex items-center justify-center font-bold">
                1
              </div>
              <div className="flex-grow">
                <h3 className="text-xl font-semibold text-white mb-2">Input Your Data</h3>
                <p className="text-gray-400">
                  Upload historical energy readings and building metadata to the platform.
                </p>
              </div>
            </motion.div>

            {/* Step 2 */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="flex gap-6 items-start"
            >
              <div className="flex-shrink-0 w-12 h-12 bg-white text-black rounded-full flex items-center justify-center font-bold">
                2
              </div>
              <div className="flex-grow">
                <h3 className="text-xl font-semibold text-white mb-2">Model Learns</h3>
                <p className="text-gray-400">
                  Our system analyzes patterns and builds a model specific to your building.
                </p>
              </div>
            </motion.div>

            {/* Step 3 */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="flex gap-6 items-start"
            >
              <div className="flex-shrink-0 w-12 h-12 bg-white text-black rounded-full flex items-center justify-center font-bold">
                3
              </div>
              <div className="flex-grow">
                <h3 className="text-xl font-semibold text-white mb-2">Get Predictions</h3>
                <p className="text-gray-400">
                  Receive accurate forecasts and actionable insights to optimize performance.
                </p>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-black px-4 py-20 border-t border-gray-800">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">Ready to see your building <span className="text-green-400">clearly</span></h2>
            <p className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto">
              Start with a prediction. See what becomes possible.
            </p>
            <Link
              href="/predict"
              className="inline-block bg-white text-black px-8 py-4 font-medium hover:bg-gray-200 transition-colors text-lg"
            >
              Make Your First Prediction
            </Link>
          </motion.div>
        </div>
      </section>
    </>
  );
}
