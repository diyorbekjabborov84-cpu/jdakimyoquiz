import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "JDA Kimyo Quiz — Admin Panel",
  description: "JDA Kimyo Quiz Telegram boti boshqaruv paneli",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="uz">
      <body>{children}</body>
    </html>
  );
}
