import type { Metadata } from "next";
import Layout from "../components/Layout";
import ThemeProvider from "../components/ThemeProvider";
import "./globals.css";

export const metadata: Metadata = {
  title: "Next.js DaisyUI App",
  description: "A Next.js app with theme switching",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning >
      <body>
        <ThemeProvider>
          <Layout>{children}</Layout>
        </ThemeProvider>
      </body>
    </html>
  );
}
