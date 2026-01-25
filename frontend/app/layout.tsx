import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Smart Building Energy",
  description: "Energy prediction and insights platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased bg-black text-white">
        <nav className="fixed top-0 left-0 right-0 z-50 bg-black border-b border-gray-800">
          <div className="max-w-6xl mx-auto px-4 py-4">
            <div className="flex gap-8">
              <a href="/" className="text-white hover:text-gray-300 transition-colors">
                Home
              </a>
              <a href="/predict" className="text-white hover:text-gray-300 transition-colors">
                Predict
              </a>
              <a href="/insights" className="text-white hover:text-gray-300 transition-colors">
                Insights
              </a>
              <a href="/impact" className="text-white hover:text-gray-300 transition-colors">
                Impact
              </a>
              <a href="/about" className="text-white hover:text-gray-300 transition-colors">
                About
              </a>
            </div>
          </div>
        </nav>
        <div className="pt-16">{children}</div>
      </body>
    </html>
  );
}
