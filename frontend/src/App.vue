<template>
  <el-container class="app-shell">
    <div class="aurora aurora-one"></div>
    <div class="aurora aurora-two"></div>

    <el-aside width="260px" class="sidebar glass-panel">
      <div class="brand">
        <div class="brand-mark">Q</div>
        <div>
          <h1>QGateway</h1>
          <span>{{ t.subtitle }}</span>
        </div>
      </div>

      <nav class="nav-list">
        <button
          v-for="item in navItems"
          :key="item.key"
          class="nav-item"
          :class="{ active: activeView === item.key }"
          @click="activeView = item.key"
        >
          <span class="nav-dot"></span>
          {{ item.label }}
        </button>
      </nav>
    </el-aside>

    <el-container class="main-shell">
      <el-header class="topbar glass-panel">
        <div>
          <strong>{{ title }}</strong>
          <span>{{ t.alpha }}</span>
        </div>
        <div class="top-actions">
          <button class="language-toggle" @click="toggleLanguage">{{ t.switchLanguage }}</button>
          <span class="status-pill" :class="health?.status === 'ok' ? 'online' : 'pending'">
            {{ health?.status === 'ok' ? t.online : t.checking }}
          </span>
        </div>
      </el-header>

      <el-main class="content">
        <DashboardView v-if="activeView === 'dashboard'" :health="health" :labels="t.dashboard" />
        <SettingsView v-else-if="activeView === 'settings'" :labels="t.settings" />
        <LogsView v-else :labels="t.logs" />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { getJson } from "./api/client";
import DashboardView from "./views/DashboardView.vue";
import LogsView from "./views/LogsView.vue";
import SettingsView from "./views/SettingsView.vue";

type Language = "zh" | "en";
type ViewKey = "dashboard" | "settings" | "logs";
type Health = {
  status: string;
  service: string;
  version: string;
  runtime: string;
  uptime_seconds: number;
};

const dictionaries = {
  zh: {
    subtitle: "开源 AI Runtime",
    alpha: "Alpha 0.1 · 液态玻璃控制台",
    online: "在线",
    checking: "检查中",
    switchLanguage: "EN",
    nav: { dashboard: "仪表盘", settings: "设置", logs: "日志" },
    dashboard: {
      backend: "后端服务",
      runtime: "运行状态",
      version: "版本",
      uptime: "运行时长",
      milestone: "里程碑 1",
      scope: "Alpha 0.1 范围",
      healthApi: "健康检查 API",
      settings: "设置",
      logs: "日志",
      launcher: "启动器",
      ready: "已就绪",
      readOnly: "只读配置",
      logViewer: "最近日志查看器",
      detectionOnly: "仅检测",
      unknown: "未知",
      checking: "检查中",
    },
    settings: {
      title: "设置",
      gateway: "网关",
      version: "版本",
      logLevel: "日志级别",
      logFile: "日志文件",
      modelPaths: "模型路径",
      launchers: "启动器",
      loading: "正在加载配置...",
    },
    logs: {
      title: "日志",
      refresh: "刷新",
      empty: "暂无日志。",
    },
  },
  en: {
    subtitle: "Open Source AI Runtime",
    alpha: "Alpha 0.1 · Liquid Glass Console",
    online: "Online",
    checking: "Checking",
    switchLanguage: "中文",
    nav: { dashboard: "Dashboard", settings: "Settings", logs: "Logs" },
    dashboard: {
      backend: "Backend",
      runtime: "Runtime",
      version: "Version",
      uptime: "Uptime",
      milestone: "Milestone 1",
      scope: "Alpha 0.1 Scope",
      healthApi: "Health API",
      settings: "Settings",
      logs: "Logs",
      launcher: "Launcher",
      ready: "Ready",
      readOnly: "Read-only",
      logViewer: "Recent file log viewer",
      detectionOnly: "Detection only",
      unknown: "Unknown",
      checking: "Checking",
    },
    settings: {
      title: "Settings",
      gateway: "Gateway",
      version: "Version",
      logLevel: "Log Level",
      logFile: "Log File",
      modelPaths: "Model Paths",
      launchers: "Launchers",
      loading: "Loading settings...",
    },
    logs: {
      title: "Logs",
      refresh: "Refresh",
      empty: "No logs yet.",
    },
  },
} as const;

const activeView = ref<ViewKey>("dashboard");
const language = ref<Language>((localStorage.getItem("qgateway-language") as Language) || "zh");
const health = ref<Health | null>(null);
const t = computed(() => dictionaries[language.value]);
const navItems = computed(() => [
  { key: "dashboard" as const, label: t.value.nav.dashboard },
  { key: "settings" as const, label: t.value.nav.settings },
  { key: "logs" as const, label: t.value.nav.logs },
]);
const title = computed(() => t.value.nav[activeView.value]);

function toggleLanguage() {
  language.value = language.value === "zh" ? "en" : "zh";
  localStorage.setItem("qgateway-language", language.value);
}

onMounted(async () => {
  health.value = await getJson<Health>("/api/v1/health");
});
</script>
