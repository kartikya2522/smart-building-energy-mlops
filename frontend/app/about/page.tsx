'use client';

import { motion } from 'framer-motion';

export default function About() {
  const fadeInUp = {
    initial: { opacity: 0, y: 20 },
    whileInView: { opacity: 1, y: 0 },
    viewport: { once: true },
    transition: { duration: 0.7 },
  };

  return (
    <main className="bg-black text-white">
      {/* Overview */}
      <section className="min-h-screen bg-black px-4 py-20 flex items-center border-b border-gray-800">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl md:text-6xl font-bold mb-8 leading-tight">
              About This <span className="text-blue-400">Platform</span>
            </h1>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="space-y-6"
            >
              <p className="text-xl text-gray-300 leading-relaxed">
                This is a machine learning system designed to predict building energy consumption. It takes environmental and temporal data as input and returns three outputs: predicted energy consumption in watt-hours, estimated cost in Indian rupees, and estimated CO2 emissions.
              </p>

              <p className="text-xl text-gray-300 leading-relaxed">
                The core prediction model is a Ridge Regression algorithm trained on historical building energy data. It learns the relationship between environmental conditions and actual energy usage, enabling accurate forecasts for new conditions.
              </p>

              <p className="text-xl text-gray-300 leading-relaxed">
                The system also provides insights into which environmental factors most strongly influence your building's energy consumption, helping operators and managers make data-informed decisions about efficiency improvements.
              </p>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-black px-4 py-20 border-b border-gray-800">
        <div className="max-w-4xl mx-auto">
          <motion.div {...fadeInUp}>
            <h2 className="text-4xl md:text-5xl font-bold mb-12">How It Works</h2>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="space-y-8"
          >
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="border-l-2 border-blue-400 pl-8 py-4"
            >
              <h3 className="text-2xl font-semibold mb-3 text-blue-400">Data Input</h3>
              <p className="text-gray-300 leading-relaxed">
                The system accepts eight environmental and temporal features: outdoor humidity, wind speed, visibility, dew point temperature, solar radiation, hour of day, and cyclical encodings of time. These features are derived from weather stations and temporal data.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="border-l-2 border-blue-400 pl-8 py-4"
            >
              <h3 className="text-2xl font-semibold mb-3 text-blue-400">Model Processing</h3>
              <p className="text-gray-300 leading-relaxed">
                A trained Ridge Regression model processes the input features. Ridge Regression is a linear regression variant that prevents overfitting through regularization. The model was trained on historical building energy data with careful feature engineering and validation.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="border-l-2 border-blue-400 pl-8 py-4"
            >
              <h3 className="text-2xl font-semibold mb-3 text-blue-400">Output Generation</h3>
              <p className="text-gray-300 leading-relaxed">
                The model outputs predicted energy consumption in watt-hours. The system then applies fixed conversion rates (5 INR per kilowatt-hour for cost, 0.82 kg CO2 per kilowatt-hour for emissions) to provide business and environmental context.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="border-l-2 border-green-400 pl-8 py-4"
            >
              <h3 className="text-2xl font-semibold mb-3 text-green-400">Insights Analysis</h3>
              <p className="text-gray-300 leading-relaxed">
                A companion insights system analyzes feature importance to identify which environmental factors most strongly influence energy consumption in your building. This enables targeted efficiency improvements.
              </p>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Technology Stack */}
      <section className="bg-black px-4 py-20 border-b border-gray-800">
        <div className="max-w-4xl mx-auto">
          <motion.div {...fadeInUp}>
            <h2 className="text-4xl md:text-5xl font-bold mb-12">Technology</h2>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Backend */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="border border-gray-700 p-8"
            >
              <h3 className="text-2xl font-semibold mb-6">Backend</h3>
              <ul className="space-y-3 text-gray-300">
                <li className="flex items-start gap-3">
                  <span className="text-white font-semibold min-w-fit">Python</span>
                  <span>Core application language</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-white font-semibold min-w-fit">FastAPI</span>
                  <span>REST API framework with automatic documentation</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-white font-semibold min-w-fit">scikit-learn</span>
                  <span>Ridge Regression and machine learning utilities</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-white font-semibold min-w-fit">MLflow</span>
                  <span>Model versioning and artifact management</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-white font-semibold min-w-fit">Pydantic</span>
                  <span>Request/response validation and documentation</span>
                </li>
              </ul>
            </motion.div>

            {/* Frontend */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="border border-gray-700 p-8"
            >
              <h3 className="text-2xl font-semibold mb-6">Frontend</h3>
              <ul className="space-y-3 text-gray-300">
                <li className="flex items-start gap-3">
                  <span className="text-white font-semibold min-w-fit">Next.js</span>
                  <span>React framework with App Router and server components</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-white font-semibold min-w-fit">TypeScript</span>
                  <span>Type-safe JavaScript for frontend logic</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-white font-semibold min-w-fit">Tailwind CSS</span>
                  <span>Utility-first styling framework</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-white font-semibold min-w-fit">Framer Motion</span>
                  <span>Production-ready animation library</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-white font-semibold min-w-fit">Fetch API</span>
                  <span>Native HTTP client for backend communication</span>
                </li>
              </ul>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Design & Architecture */}
      <section className="bg-black px-4 py-20 border-b border-gray-800">
        <div className="max-w-4xl mx-auto">
          <motion.div {...fadeInUp}>
            <h2 className="text-4xl md:text-5xl font-bold mb-12">Architecture</h2>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="border border-gray-700 p-8 space-y-6"
          >
            <div>
              <h3 className="text-xl font-semibold mb-3">Frontend-Backend Separation</h3>
              <p className="text-gray-300 leading-relaxed">
                The frontend is a Next.js application that communicates with a FastAPI backend via REST API calls. The frontend handles user interface, form validation, and result presentation. The backend handles all machine learning inference, feature engineering, and business logic.
              </p>
            </div>

            <div>
              <h3 className="text-xl font-semibold mb-3">API-First Design</h3>
              <p className="text-gray-300 leading-relaxed">
                All backend functionality is exposed through HTTP endpoints with documented request and response schemas. This allows the frontend to be developed independently and enables future integrations with other systems.
              </p>
            </div>

            <div>
              <h3 className="text-xl font-semibold mb-3">Model Versioning</h3>
              <p className="text-gray-300 leading-relaxed">
                Trained models are versioned and stored using MLflow. This ensures reproducibility, enables easy model updates, and maintains a complete audit trail of deployed models.
              </p>
            </div>

            <div>
              <h3 className="text-xl font-semibold mb-3">Development & Deployment</h3>
              <p className="text-gray-300 leading-relaxed">
                Both frontend and backend run locally with hot reload during development. The backend server runs on port 8000 with automatic API documentation available at /docs. The frontend development server runs on port 3000.
              </p>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Closing */}
      <section className="bg-black px-4 py-20">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-8 leading-tight">
              Built for <span className="text-blue-400">clarity</span> and <span className="text-green-400">impact</span>
            </h2>

            <p className="text-xl text-gray-300 max-w-2xl leading-relaxed mb-8">
              This platform demonstrates how careful machine learning engineering, thoughtful feature design, and clean system architecture can create practical tools for real-world problems. It prioritizes accuracy, interpretability, and usability over complexity.
            </p>

            <p className="text-lg text-gray-400">
              For technical questions or to review the system architecture, visit the API documentation at http://localhost:8000/docs.
            </p>
          </motion.div>
        </div>
      </section>
    </main>
  );
}
