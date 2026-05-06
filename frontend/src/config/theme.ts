import type { ThemeConfig } from 'antd';

export const astraTheme: ThemeConfig = {
  token: {
    colorPrimary: '#1677ff',
    colorSuccess: '#16c784',
    colorError: '#ff4d4f',
    colorWarning: '#f5a524',
    colorInfo: '#7c5cff',
    colorTextBase: '#e6edf7',
    colorBgBase: '#07111f',
    colorBorder: '#1f3550',
    borderRadius: 8,
    fontFamily:
      'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
  },
  components: {
    Layout: {
      bodyBg: '#07111f',
      headerBg: '#07111f',
      siderBg: '#06101d',
      triggerBg: '#0d1b2a',
    },
    Menu: {
      darkItemBg: '#06101d',
      darkSubMenuItemBg: '#06101d',
      darkItemSelectedBg: '#123a74',
      darkItemHoverBg: '#0d253f',
      itemBorderRadius: 8,
    },
    Card: {
      colorBgContainer: '#0d1b2a',
      colorBorderSecondary: '#1f3550',
    },
    Table: {
      colorBgContainer: '#0d1b2a',
      headerBg: '#102137',
      rowHoverBg: '#102137',
      borderColor: '#1f3550',
    },
    Button: {
      borderRadius: 8,
    },
    Input: {
      colorBgContainer: '#0a1625',
      colorBorder: '#1f3550',
    },
    Select: {
      colorBgContainer: '#0a1625',
      colorBorder: '#1f3550',
    },
  },
};
