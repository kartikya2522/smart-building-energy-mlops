'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';

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
        <div className="absolute inset-0 z-0">
          {/* Large rotating circle - outer energy field */}
          <motion.div
            className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full blur-2xl"
            style={{
              background: 'radial-gradient(circle, rgba(74, 222, 128, 0.5) 0%, transparent 70%)',
            }}
            animate={{ rotate: 360 }}
            transition={{ duration: 40, repeat: Infinity, ease: 'linear' }}
          />

          {/* Second rotating circle - offset */}
          <motion.div
            className="absolute top-1/3 right-1/4 w-80 h-80 rounded-full blur-2xl"
            style={{
              background: 'radial-gradient(circle, rgba(96, 165, 250, 0.4) 0%, transparent 70%)',
            }}
            animate={{ rotate: -360 }}
            transition={{ duration: 50, repeat: Infinity, ease: 'linear' }}
          />

          {/* Third subtle circle - float effect */}
          <motion.div
            className="absolute bottom-1/4 left-1/3 w-72 h-72 rounded-full blur-2xl"
            style={{
              background: 'radial-gradient(circle, rgba(34, 197, 94, 0.4) 0%, transparent 70%)',
            }}
            animate={{ y: [0, 20, -20, 0] }}
            transition={{ duration: 12, repeat: Infinity, ease: 'easeInOut' }}
          />

          {/* SVG accent lines - subtle energy flows */}
          <svg
            className="absolute inset-0 w-full h-full opacity-20"
            preserveAspectRatio="xMidYMid slice"
            viewBox="0 0 1200 800"
          >
            <defs>
              <linearGradient id="flowGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#4ade80" />
                <stop offset="50%" stopColor="#60a5fa" />
                <stop offset="100%" stopColor="#4ade80" />
              </linearGradient>
            </defs>

            {/* Concentric circles representing Earth / energy layers */}
            <motion.circle
              cx="600"
              cy="400"
              r="200"
              fill="none"
              stroke="url(#flowGradient)"
              strokeWidth="1"
              animate={{ opacity: [0.2, 0.5, 0.2] }}
              transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
            />
            <motion.circle
              cx="600"
              cy="400"
              r="260"
              fill="none"
              stroke="url(#flowGradient)"
              strokeWidth="0.5"
              animate={{ opacity: [0.1, 0.3, 0.1] }}
              transition={{ duration: 5, repeat: Infinity, ease: 'easeInOut', delay: 0.3 }}
            />
            <motion.circle
              cx="600"
              cy="400"
              r="140"
              fill="none"
              stroke="url(#flowGradient)"
              strokeWidth="1"
              animate={{ opacity: [0.15, 0.4, 0.15] }}
              transition={{ duration: 3.5, repeat: Infinity, ease: 'easeInOut', delay: 0.6 }}
            />

            {/* Subtle energy lines */}
            <motion.line
              x1="600"
              y1="150"
              x2="600"
              y2="650"
              stroke="#60a5fa"
              strokeWidth="0.5"
              animate={{ opacity: [0.1, 0.25, 0.1] }}
              transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
            />
            <motion.line
              x1="350"
              y1="400"
              x2="850"
              y2="400"
              stroke="#4ade80"
              strokeWidth="0.5"
              animate={{ opacity: [0.08, 0.2, 0.08] }}
              transition={{ duration: 4.5, repeat: Infinity, ease: 'easeInOut', delay: 0.2 }}
            />
          </svg>
        </div>

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
