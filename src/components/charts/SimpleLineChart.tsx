import { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

interface SimpleLineChartProps {
  data?: number[];
  color?: string;
  height?: number;
}

const fallbackData = [10, 18, 16, 28, 34, 31, 46, 52, 48, 63, 72, 89, 84, 102, 128];

export function SimpleLineChart({ data = fallbackData, color = '#1677ff', height = 160 }: SimpleLineChartProps) {
  const ref = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!ref.current) return;
    const chart = echarts.init(ref.current);
    chart.setOption({
      backgroundColor: 'transparent',
      grid: { left: 8, right: 8, top: 8, bottom: 8 },
      xAxis: { type: 'category', show: false, data: data.map((_, index) => index) },
      yAxis: { type: 'value', show: false },
      series: [
        {
          type: 'line',
          data,
          smooth: true,
          symbol: 'none',
          lineStyle: { color, width: 2 },
          areaStyle: { color: `${color}22` },
        },
      ],
    });
    const handleResize = () => chart.resize();
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
      chart.dispose();
    };
  }, [color, data]);

  return <div ref={ref} style={{ height, width: '100%' }} />;
}
