import type { ReactNode } from 'react';

import styles from './PageContainer.module.css';

interface PageContainerProps {
  title: string;
  description?: string;
  extra?: ReactNode;
  actions?: ReactNode;
  children: ReactNode;
}

export function PageContainer({ title, description, extra, actions, children }: PageContainerProps) {
  return (
    <main className={styles.pageContainer}>
      <header className={styles.pageHeader}>
        <div>
          <h1 className={styles.title}>{title}</h1>
          {description ? <p className={styles.description}>{description}</p> : null}
        </div>
        {extra || actions ? <div className={styles.actions}>{extra ?? actions}</div> : null}
      </header>
      <section className={styles.content}>{children}</section>
    </main>
  );
}
