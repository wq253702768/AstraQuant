import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import type { PropsWithChildren } from 'react';

import { QueryProvider } from './QueryProvider';
import { astraTheme } from '../../config/theme';

export function AppProviders({ children }: PropsWithChildren) {
  return (
    <ConfigProvider locale={zhCN} theme={astraTheme}>
      <QueryProvider>{children}</QueryProvider>
    </ConfigProvider>
  );
}
