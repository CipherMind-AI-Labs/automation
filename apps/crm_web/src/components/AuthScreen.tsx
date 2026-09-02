"use client";

import { useState } from "react";
import styles from "@/components/crm.module.css";

interface AuthScreenProps {
  onAuthenticate: (token: string) => Promise<boolean>;
  isVerifying: boolean;
  error: string | null;
}

export function AuthScreen({ onAuthenticate, isVerifying, error }: AuthScreenProps): React.JSX.Element {
  const [tokenInput, setTokenInput] = useState("");

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!tokenInput.trim() || isVerifying) return;
    await onAuthenticate(tokenInput.trim());
  };

  return (
    <div className={styles.authShell}>
      <div className={styles.authCard}>
        <div className={styles.authHeader}>
          <img src="/logo-full.png" alt="CipherMind AI Labs" className={styles.brandLogo} />
          <p className={styles.eyebrow}>CipherMind AI Labs LLC</p>
          <h1>Lead Discovery & CRM</h1>
          <p className={styles.authSubtitle}>
            Enter your CRM Access Token to access the operational workspace.
          </p>
        </div>

        <form onSubmit={handleSubmit} className={styles.authForm}>
          {error && <div className={styles.errorBanner}>{error}</div>}

          <label className={styles.authLabel}>
            <span>Access Token</span>
            <input
              type="password"
              value={tokenInput}
              onChange={(e) => setTokenInput(e.target.value)}
              placeholder="Enter access token…"
              autoFocus
              required
            />
          </label>

          <button
            type="submit"
            className={styles.primaryButton}
            disabled={!tokenInput.trim() || isVerifying}
          >
            {isVerifying ? "Verifying Token…" : "Authenticate Session"}
          </button>
        </form>

        <footer className={styles.authFooter}>
          <span>Protected Operational System</span>
        </footer>
      </div>
    </div>
  );
}
