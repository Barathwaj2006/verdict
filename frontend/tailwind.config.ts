import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        obsidian: {
          950: "#07080C",
          900: "#0D0F17",
          800: "#131624",
          700: "#1D2236",
        },
        agent: {
          lead: "#818CF8",
          landscape: "#38BDF8",
          feasibility: "#F59E0B",
          opportunity: "#10B981",
          skeptic: "#F43F5E",
          verifier: "#34D399",
        },
      },
      animation: {
        "pulse-glow": "pulseGlow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "float-subtle": "floatSubtle 6s ease-in-out infinite",
      },
      keyframes: {
        pulseGlow: {
          "0%, 100%": { opacity: "1", filter: "brightness(1.2)" },
          "50%": { opacity: "0.6", filter: "brightness(0.9)" },
        },
        floatSubtle: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-6px)" },
        },
      },
    },
  },
  plugins: [],
};
export default config;
