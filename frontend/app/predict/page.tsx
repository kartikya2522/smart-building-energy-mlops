'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';

interface PredictionResult {
  energy_wh: number;
  cost_inr: number;
  co2_kg: number;
}

interface FormData {
  RH_6: string;
  Windspeed: string;
  Visibility: string;
  Tdewpoint: string;
  rv1: string;
  hour: string;
  hour_sin: string;
  hour_cos: string;
}

export default function Predict() {
  const [formData, setFormData] = useState<FormData>({
    RH_6: '50',
    Windspeed: '5',
    Visibility: '10',
    Tdewpoint: '15',
    rv1: '100',
    hour: '12',
    hour_sin: '0.5',
    hour_cos: '0.5',
  });

  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const payload = {
        RH_6: parseFloat(formData.RH_6),
        Windspeed: parseFloat(formData.Windspeed),
        Visibility: parseFloat(formData.Visibility),
        Tdewpoint: parseFloat(formData.Tdewpoint),
        rv1: parseFloat(formData.rv1),
        hour: parseFloat(formData.hour),
        hour_sin: parseFloat(formData.hour_sin),
        hour_cos: parseFloat(formData.hour_cos),
      };

      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Prediction failed');
      }

      const data: PredictionResult = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
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
            Predict Energy
          </h1>
          <p className="text-xl text-gray-400 max-w-2xl">
            Enter environmental conditions to forecast energy consumption, estimated cost, and carbon impact.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Input Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="border border-gray-700 p-8 bg-black"
          >
            <h2 className="text-2xl font-semibold text-white mb-6">Input Parameters</h2>

            <form onSubmit={handlePredict} className="space-y-6">
              {/* Row 1 */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    RH_6 (%) - Humidity
                  </label>
                  <input
                    type="number"
                    name="RH_6"
                    value={formData.RH_6}
                    onChange={handleInputChange}
                    min="0"
                    max="100"
                    step="0.1"
                    className="w-full bg-gray-900 border border-gray-700 text-white px-4 py-2 focus:outline-none focus:border-white"
                  />
                  <p className="text-xs text-gray-500 mt-1">0-100</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Windspeed (m/s)
                  </label>
                  <input
                    type="number"
                    name="Windspeed"
                    value={formData.Windspeed}
                    onChange={handleInputChange}
                    min="0"
                    step="0.1"
                    className="w-full bg-gray-900 border border-gray-700 text-white px-4 py-2 focus:outline-none focus:border-white"
                  />
                  <p className="text-xs text-gray-500 mt-1">≥ 0</p>
                </div>
              </div>

              {/* Row 2 */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Visibility (km)
                  </label>
                  <input
                    type="number"
                    name="Visibility"
                    value={formData.Visibility}
                    onChange={handleInputChange}
                    min="0"
                    step="0.1"
                    className="w-full bg-gray-900 border border-gray-700 text-white px-4 py-2 focus:outline-none focus:border-white"
                  />
                  <p className="text-xs text-gray-500 mt-1">≥ 0</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Tdewpoint (°C)
                  </label>
                  <input
                    type="number"
                    name="Tdewpoint"
                    value={formData.Tdewpoint}
                    onChange={handleInputChange}
                    min="-50"
                    max="50"
                    step="0.1"
                    className="w-full bg-gray-900 border border-gray-700 text-white px-4 py-2 focus:outline-none focus:border-white"
                  />
                  <p className="text-xs text-gray-500 mt-1">-50 to 50</p>
                </div>
              </div>

              {/* Row 3 */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    rv1 (Wh/m²) - Radiation
                  </label>
                  <input
                    type="number"
                    name="rv1"
                    value={formData.rv1}
                    onChange={handleInputChange}
                    min="0"
                    step="0.1"
                    className="w-full bg-gray-900 border border-gray-700 text-white px-4 py-2 focus:outline-none focus:border-white"
                  />
                  <p className="text-xs text-gray-500 mt-1">≥ 0</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Hour (0-23)
                  </label>
                  <input
                    type="number"
                    name="hour"
                    value={formData.hour}
                    onChange={handleInputChange}
                    min="0"
                    max="23"
                    step="1"
                    className="w-full bg-gray-900 border border-gray-700 text-white px-4 py-2 focus:outline-none focus:border-white"
                  />
                  <p className="text-xs text-gray-500 mt-1">0-23</p>
                </div>
              </div>

              {/* Row 4 */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Hour Sin
                  </label>
                  <input
                    type="number"
                    name="hour_sin"
                    value={formData.hour_sin}
                    onChange={handleInputChange}
                    min="-1"
                    max="1"
                    step="0.01"
                    className="w-full bg-gray-900 border border-gray-700 text-white px-4 py-2 focus:outline-none focus:border-white"
                  />
                  <p className="text-xs text-gray-500 mt-1">-1 to 1</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Hour Cos
                  </label>
                  <input
                    type="number"
                    name="hour_cos"
                    value={formData.hour_cos}
                    onChange={handleInputChange}
                    min="-1"
                    max="1"
                    step="0.01"
                    className="w-full bg-gray-900 border border-gray-700 text-white px-4 py-2 focus:outline-none focus:border-white"
                  />
                  <p className="text-xs text-gray-500 mt-1">-1 to 1</p>
                </div>
              </div>

              {/* Error Message */}
              {error && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-red-900/30 border border-red-700 text-red-300 px-4 py-3 text-sm"
                >
                  {error}
                </motion.div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-white text-black px-6 py-3 font-medium hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Predicting...' : 'Predict'}
              </button>
            </form>
          </motion.div>

          {/* Results Section */}
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="border border-gray-700 p-8 bg-black"
            >
              <h2 className="text-2xl font-semibold text-white mb-8">Prediction Results</h2>

              <div className="space-y-6">
                {/* Energy */}
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0 }}
                  className="border border-gray-700 p-6 hover:border-blue-500/30 transition-colors"
                >
                  <p className="text-gray-400 text-sm mb-2">Energy Consumption</p>
                  <p className="text-4xl font-bold text-blue-400">
                    {result.energy_wh.toFixed(2)}
                  </p>
                  <p className="text-gray-500 text-sm mt-2">Watt-hours (Wh)</p>
                </motion.div>

                {/* Cost */}
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.1 }}
                  className="border border-gray-700 p-6 hover:border-green-500/30 transition-colors"
                >
                  <p className="text-gray-400 text-sm mb-2">Estimated Cost</p>
                  <p className="text-4xl font-bold text-green-400">
                    {result.cost_inr.toFixed(2)}
                  </p>
                  <p className="text-gray-500 text-sm mt-2">Indian Rupees (INR)</p>
                </motion.div>

                {/* CO2 */}
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                  className="border border-gray-700 p-6 hover:border-green-500/30 transition-colors"
                >
                  <p className="text-gray-400 text-sm mb-2">CO2 Emissions</p>
                  <p className="text-4xl font-bold text-green-400">
                    {result.co2_kg.toFixed(4)}
                  </p>
                  <p className="text-gray-500 text-sm mt-2">Kilograms (kg)</p>
                </motion.div>
              </div>
            </motion.div>
          )}

          {/* Empty State */}
          {!result && !loading && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="border border-dashed border-gray-700 p-8 flex items-center justify-center bg-black/50"
            >
              <p className="text-gray-500 text-center">
                Results will appear here after prediction
              </p>
            </motion.div>
          )}
        </div>
      </div>
    </main>
  );
}
