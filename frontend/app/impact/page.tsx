'use client';

import { motion } from 'framer-motion';

export default function Impact() {
  const fadeInUp = {
    initial: { opacity: 0, y: 20 },
    whileInView: { opacity: 1, y: 0 },
    viewport: { once: true },
    transition: { duration: 0.7 },
  };

  const containerVariants = {
    initial: { opacity: 0 },
    whileInView: { opacity: 1 },
    viewport: { once: true },
  };

  const itemVariants = {
    initial: { opacity: 0, y: 15 },
    whileInView: { opacity: 1, y: 0 },
    transition: { duration: 0.6 },
  };

  return (
    <main className="bg-black text-white">
      {/* Intro Section */}
      <section className="min-h-screen bg-black px-4 py-20 flex items-center">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl md:text-6xl font-bold mb-8 leading-tight">
              Energy clarity enables climate progress
            </h1>

            <motion.p
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-xl md:text-2xl text-gray-300 max-w-2xl leading-relaxed"
            >
              Buildings consume nearly 40% of global energy and produce 30% of energy-related carbon emissions. Most lack visibility into their consumption patterns. This absence of understanding prevents meaningful action.
            </motion.p>
          </motion.div>
        </div>
      </section>

      {/* Why It Matters */}
      <section className="bg-black px-4 py-20 border-t border-gray-800">
        <div className="max-w-4xl mx-auto">
          <motion.div {...fadeInUp}>
            <h2 className="text-4xl md:text-5xl font-bold mb-12">Why Clarity Matters</h2>
          </motion.div>

          <motion.div
            variants={containerVariants}
            initial="initial"
            whileInView="whileInView"
            viewport={{ once: true }}
            className="space-y-8"
          >
            <motion.div variants={itemVariants} className="border-l-2 border-white pl-8 py-4">
              <p className="text-xl text-gray-300 leading-relaxed">
                Without prediction, building operators make decisions based on incomplete information. Energy consumption seems random. Costs appear inevitable. Opportunities for improvement remain hidden.
              </p>
            </motion.div>

            <motion.div variants={itemVariants} className="border-l-2 border-white pl-8 py-4">
              <p className="text-xl text-gray-300 leading-relaxed">
                Prediction transforms this blindness into sight. When you understand how external factors influence consumption, you can anticipate demand, optimize operations, and reduce waste. Small changes compound.
              </p>
            </motion.div>

            <motion.div variants={itemVariants} className="border-l-2 border-white pl-8 py-4">
              <p className="text-xl text-gray-300 leading-relaxed">
                This platform makes that clarity accessible. It takes the complexity out of understanding building performance and puts actionable insights in your hands.
              </p>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Real-World Impact */}
      <section className="bg-black px-4 py-20 border-t border-gray-800">
        <div className="max-w-4xl mx-auto">
          <motion.div {...fadeInUp}>
            <h2 className="text-4xl md:text-5xl font-bold mb-12">Real-World Impact</h2>
          </motion.div>

          <motion.div
            variants={containerVariants}
            initial="initial"
            whileInView="whileInView"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8"
          >
            {/* Cost */}
            <motion.div variants={itemVariants} className="border border-gray-700 p-8">
              <h3 className="text-2xl font-semibold mb-4">Lower Costs</h3>
              <p className="text-gray-300 leading-relaxed mb-4">
                Precise predictions enable smarter scheduling and load management, reducing energy bills by 10-20% without sacrificing comfort or productivity.
              </p>
              <p className="text-sm text-gray-500">
                For a typical office building, that means tens of thousands in annual savings.
              </p>
            </motion.div>

            {/* Efficiency */}
            <motion.div variants={itemVariants} className="border border-gray-700 p-8">
              <h3 className="text-2xl font-semibold mb-4">Better Efficiency</h3>
              <p className="text-gray-300 leading-relaxed mb-4">
                Understanding energy patterns reveals where efficiency improvements will have the most impact. You optimize where it matters.
              </p>
              <p className="text-sm text-gray-500">
                Data-driven decisions beat guesswork every time.
              </p>
            </motion.div>

            {/* Emissions */}
            <motion.div variants={itemVariants} className="border border-gray-700 p-8">
              <h3 className="text-2xl font-semibold mb-4">Lower Emissions</h3>
              <p className="text-gray-300 leading-relaxed mb-4">
                Every unit of energy saved is energy that doesn't need to be produced. Every prediction-enabled optimization reduces your building's carbon footprint.
              </p>
              <p className="text-sm text-gray-500">
                Measurable, meaningful climate action.
              </p>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* How It Works in Practice */}
      <section className="bg-black px-4 py-20 border-t border-gray-800">
        <div className="max-w-4xl mx-auto">
          <motion.div {...fadeInUp}>
            <h2 className="text-4xl md:text-5xl font-bold mb-12">From Insight to Action</h2>
          </motion.div>

          <motion.div
            variants={containerVariants}
            initial="initial"
            whileInView="whileInView"
            viewport={{ once: true }}
            className="space-y-8"
          >
            <motion.div variants={itemVariants} className="border border-gray-700 p-8 hover:border-green-500/30 transition-colors">
              <div className="flex gap-6 items-start">
                <div className="flex-shrink-0 w-10 h-10 bg-green-500 text-black rounded-full flex items-center justify-center font-bold">
                  1
                </div>
                <div className="flex-grow">
                  <h3 className="text-xl font-semibold text-white mb-3">See Your Building</h3>
                  <p className="text-gray-300 leading-relaxed">
                    Predict how weather, time, and external conditions will affect your building's energy consumption. Understand the patterns that drive your costs.
                  </p>
                </div>
              </div>
            </motion.div>

            <motion.div variants={itemVariants} className="border border-gray-700 p-8 hover:border-green-500/30 transition-colors">
              <div className="flex gap-6 items-start">
                <div className="flex-shrink-0 w-10 h-10 bg-green-500 text-black rounded-full flex items-center justify-center font-bold">
                  2
                </div>
                <div className="flex-grow">
                  <h3 className="text-xl font-semibold text-white mb-3">Identify Opportunities</h3>
                  <p className="text-gray-300 leading-relaxed">
                    Learn which factors have the biggest impact on your energy consumption. Focus your efforts where they will make the most difference.
                  </p>
                </div>
              </div>
            </motion.div>

            <motion.div variants={itemVariants} className="border border-gray-700 p-8 hover:border-green-500/30 transition-colors">
              <div className="flex gap-6 items-start">
                <div className="flex-shrink-0 w-10 h-10 bg-green-500 text-black rounded-full flex items-center justify-center font-bold">
                  3
                </div>
                <div className="flex-grow">
                  <h3 className="text-xl font-semibold text-white mb-3">Measure Results</h3>
                  <p className="text-gray-300 leading-relaxed">
                    Track improvements in real-time. Understand the cost savings, efficiency gains, and carbon impact of your decisions.
                  </p>
                </div>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Closing */}
      <section className="bg-black px-4 py-20 border-t border-gray-800">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-8 leading-tight">
              Climate action begins with <span className="text-green-400">understanding</span>
            </h2>

            <p className="text-xl text-gray-300 max-w-2xl mx-auto mb-10 leading-relaxed">
              This platform exists to make building energy performance transparent and actionable. Not for its own sake, but because clear information enables better decisions. And better decisions compound into real change.
            </p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8, delay: 0.2 }}
            >
              <a
                href="/predict"
                className="inline-block bg-white text-black px-8 py-4 font-medium hover:bg-gray-200 transition-colors text-lg"
              >
                Start Understanding Your Building
              </a>
            </motion.div>
          </motion.div>
        </div>
      </section>
    </main>
  );
}
