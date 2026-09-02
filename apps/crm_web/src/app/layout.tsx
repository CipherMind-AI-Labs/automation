import type { Metadata } from "next";
import "@/app/globals.css";

export const metadata: Metadata = { title: "Lead CRM", description: "Internal operational lead CRM" };

/** Defines the shared document shell for the internal CRM. */
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>): React.JSX.Element { return <html lang="en"><body>{children}</body></html>; }
