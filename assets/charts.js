(function () {
  var style = getComputedStyle(document.documentElement);
  var accent = style.getPropertyValue('--accent').trim();
  var accent2 = style.getPropertyValue('--accent2').trim();
  var ink = style.getPropertyValue('--ink').trim();
  var muted = style.getPropertyValue('--muted').trim();
  var rule = style.getPropertyValue('--rule').trim();
  var bg2 = style.getPropertyValue('--bg2').trim();

  /* =========================================================
   * 全局数据约定（定时任务依赖）
   * window.__RADAR_GAP__   : { jd:[7], me:[7] }  能力差距雷达（全周期）
   * window.__RADAR_DAILY__ : [6]                  每日学习执行雷达（7 天滚动）
   * 定时任务只需替换数组值再调用对应渲染函数即可刷新，无需改本文件。
   * ========================================================= */

  // ---- 维度定义（与"四、能力差距分析"表格严格一致，7 维） ----
  var GAP_INDICATORS = [
    { name: 'RAG全链路', max: 100 },
    { name: 'Agent编排', max: 100 },
    { name: 'Spring AI', max: 100 },
    { name: '分布式中间件', max: 100 },
    { name: '工程化', max: 100 },
    { name: 'Python', max: 100 },
    { name: '面试原理深度', max: 100 }
  ];

  // ---- 全局数据：能力差距雷达（全周期）----
  // jd = JD 要求高度（0-100），me = 我当前水平（0-100，按差距表"你的现状"定性填）
  window.__RADAR_GAP__ = {
    jd: [90, 90, 85, 80, 85, 70, 90],
    me: [48, 41, 14, 30, 46, 9, 27]
  };

  // ---- 全局数据：每日学习执行雷达（7 天滚动，6 维）----
  // 维度顺序固定：计划完成率 / 学习时长 / 知识输入 / 实战输出 / 复习覆盖 / 连续打卡
  window.__RADAR_DAILY__ = [42, 50, 55, 52, 35, 15];

  var DAILY_INDICATORS = [
    { name: '计划完成率', max: 100 },
    { name: '学习时长', max: 100 },
    { name: '知识输入', max: 100 },
    { name: '实战输出', max: 100 },
    { name: '复习覆盖', max: 100 },
    { name: '连续打卡', max: 100 }
  ];

  /* ---- 渲染函数：能力差距雷达（全周期）---- */
  window.__renderGapRadar = function () {
    var el = document.getElementById('chart-gap-radar');
    if (!el || typeof echarts === 'undefined') return;
    var chart = echarts.init(el, null, { renderer: 'svg' });
    chart.setOption({
      animation: false,
      tooltip: { appendToBody: true },
      legend: {
        data: ['JD 要求', '我当前水平'],
        top: 0,
        textStyle: { color: muted, fontSize: 13 }
      },
      radar: {
        center: ['50%', '58%'],
        radius: '62%',
        indicator: GAP_INDICATORS,
        axisName: { color: ink, fontSize: 12 },
        splitLine: { lineStyle: { color: rule } },
        splitArea: { areaStyle: { color: ['transparent', bg2] } },
        axisLine: { lineStyle: { color: rule } }
      },
      series: [{
        type: 'radar',
        data: [
          {
            value: window.__RADAR_GAP__.jd,
            name: 'JD 要求',
            areaStyle: { color: accent + '22' },
            lineStyle: { color: accent, width: 2 },
            itemStyle: { color: accent }
          },
          {
            value: window.__RADAR_GAP__.me,
            name: '我当前水平',
            areaStyle: { color: accent2 + '22' },
            lineStyle: { color: accent2, width: 2, type: 'dashed' },
            itemStyle: { color: accent2 }
          }
        ]
      }]
    });
    window.addEventListener('resize', function () { chart.resize(); });
    return chart;
  };

  /* ---- 渲染函数：每日学习执行雷达（7 天滚动）---- */
  window.__renderDailyRadar = function () {
    var el = document.getElementById('chart-daily-radar');
    if (!el || typeof echarts === 'undefined') return;
    var chart = echarts.init(el, null, { renderer: 'svg' });
    chart.setOption({
      animation: false,
      tooltip: { appendToBody: true },
      legend: {
        data: ['近 7 天执行度'],
        top: 0,
        textStyle: { color: muted, fontSize: 13 }
      },
      radar: {
        center: ['50%', '56%'],
        radius: '62%',
        indicator: DAILY_INDICATORS,
        axisName: { color: ink, fontSize: 12 },
        splitLine: { lineStyle: { color: rule } },
        splitArea: { areaStyle: { color: ['transparent', bg2] } },
        axisLine: { lineStyle: { color: rule } }
      },
      series: [{
        type: 'radar',
        data: [
          {
            value: window.__RADAR_DAILY__,
            name: '近 7 天执行度',
            areaStyle: { color: accent + '22' },
            lineStyle: { color: accent, width: 2 },
            itemStyle: { color: accent }
          }
        ]
      }]
    });
    window.addEventListener('resize', function () { chart.resize(); });
    return chart;
  };

  // ---- 初始渲染 ----
  window.__renderGapRadar();
  window.__renderDailyRadar();
})();
