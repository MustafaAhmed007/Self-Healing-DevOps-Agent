import Link from 'next/link';
import './globals.css';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body><header><strong>Self-Healing DevOps Agent</strong><nav><Link href="/">Runs</Link><Link href="/architecture">Architecture</Link></nav></header>{children}</body></html>;
}
