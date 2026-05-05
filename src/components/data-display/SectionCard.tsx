import type { ReactNode } from 'react';

import styles from './SectionCard.module.css';

interface SectionCardProps {
  title?: string;
  extra?: ReactNode;
  children: ReactNode;
  className?: string;
}

export function SectionCard({ title, extra, children, className }: SectionCardProps) {
  return (
    <section className={`${styles.card} ${className ?? ''}`}>
      {(title || extra) && (
        <div className={styles.header}>
          <h3>{title}</h3>
          {extra}
        </div>
      )}
      {children}
    </section>
  );
}
