import "@/styles/globals.css";
import { Inter } from "@next/font/google";
import type { AppProps } from "next/app";
const poppins = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  weight: ["300", "400", "500", "600", "700", "800"],
});

export default function App({ Component, pageProps }: AppProps) {
  return (
    <div className={`${poppins.variable} font-sans`} >
      <Component {...pageProps} />
    </div>
  );
}
