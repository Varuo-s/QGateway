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
        <button v-for="item in navItems" :key="item.key" class="nav-item" :class="{ active: activeView === item.key }" @click="activeView = item.key">
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
        <RuntimeView v-else-if="activeView === 'runtime'" :labels="t.runtime" />
        <ModelsView v-else-if="activeView === 'models'" :labels="t.models" />
        <PlaygroundView v-else-if="activeView === 'playground'" :labels="t.playground" />
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
import ModelsView from "./views/ModelsView.vue";
import PlaygroundView from "./views/PlaygroundView.vue";
import RuntimeView from "./views/RuntimeView.vue";
import SettingsView from "./views/SettingsView.vue";

type Language = "zh" | "en";
type ViewKey = "dashboard" | "runtime" | "models" | "playground" | "settings" | "logs";
type Health = { status: string; service: string; version: string; runtime: string; uptime_seconds: number };

const dictionaries = {
  zh: {
    subtitle: "开源 AI Runtime",
    alpha: "Alpha 0.5 · 液态玻璃控制台",
    online: "在线",
    checking: "检查中",
    switchLanguage: "EN",
    nav: { dashboard: "仪表盘", runtime: "运行时", models: "模型", playground: "Playground", settings: "设置", logs: "日志" },
    dashboard: { backend: "后端服务", runtime: "运行状态", version: "版本", uptime: "运行时长", milestone: "里程碑 1", scope: "Alpha 0.1 范围", healthApi: "健康检查 API", settings: "设置", logs: "日志", launcher: "启动器", ready: "已就绪", readOnly: "只读配置", logViewer: "最近日志查看器", detectionOnly: "仅检测", unknown: "未知", checking: "检查中" },
    runtime: { title: "运行时", subtitle: "管理 llama.cpp 服务", start: "启动", stop: "停止", refresh: "刷新", state: "状态", provider: "Provider", pid: "PID", endpoint: "端点", executable: "可执行文件", model: "模型", command: "启动命令", exists: "存在", missing: "缺失", error: "错误", running: "运行中", stopped: "已停止", unknown: "未知" },
    models: { title: "模型", subtitle: "扫描本地 GGUF 模型", rescan: "重新扫描", empty: "没有发现 GGUF 模型。", count: "模型数量", scanTime: "扫描时间", name: "名称", size: "大小", format: "格式", quantization: "量化", path: "路径", unknown: "未知", loading: "正在扫描模型..." },
    playground: { title: "Playground", subtitle: "通过 /v1/responses 测试本地模型", placeholder: "输入消息，按 Ctrl + Enter 发送", send: "发送", clear: "清空", parameters: "参数", temperature: "Temperature", topP: "Top P", maxTokens: "Max Tokens", systemPrompt: "System Prompt", systemPlaceholder: "可选：输入系统提示词", user: "你", assistant: "助手", empty: "还没有消息。先发送一句话。", thinking: "模型生成中...", error: "请求失败" },
    settings: { title: "设置", gateway: "网关", version: "版本", logLevel: "日志级别", logFile: "日志文件", modelPaths: "模型路径", launchers: "启动器", loading: "正在加载配置..." },
    logs: { title: "日志", refresh: "刷新", empty: "暂无日志。" },
  },
  en: {
    subtitle: "Open Source AI Runtime",
    alpha: "Alpha 0.5 · Liquid Glass Console",
    online: "Online",
    checking: "Checking",
    switchLanguage: "中文",
    nav: { dashboard: "Dashboard", runtime: "Runtime", models: "Models", playground: "Playground", settings: "Settings", logs: "Logs" },
    dashboard: { backend: "Backend", runtime: "Runtime", version: "Version", uptime: "Uptime", milestone: "Milestone 1", scope: "Alpha 0.1 Scope", healthApi: "Health API", settings: "Settings", logs: "Logs", launcher: "Launcher", ready: "Ready", readOnly: "Read-only", logViewer: "Recent file log viewer", detectionOnly: "Detection only", unknown: "Unknown", checking: "Checking" },
    runtime: { title: "Runtime", subtitle: "Manage llama.cpp service", start: "Start", stop: "Stop", refresh: "Refresh", state: "State", provider: "Provider", pid: "PID", endpoint: "Endpoint", executable: "Executable", model: "Model", command: "Command", exists: "Exists", missing: "Missing", error: "Error", running: "Running", stopped: "Stopped", unknown: "Unknown" },
    models: { title: "Models", subtitle: "Scan local GGUF models", rescan: "Rescan", empty: "No GGUF models found.", count: "Model Count", scanTime: "Scan Time", name: "Name", size: "Size", format: "Format", quantization: "Quantization", path: "Path", unknown: "Unknown", loading: "Scanning models..." },
    playground: { title: "Playground", subtitle: "Test local models through /v1/responses", placeholder: "Type a message, Ctrl + Enter to send", send: "Send", clear: "Clear", parameters: "Parameters", temperature: "Temperature", topP: "Top P", maxTokens: "Max Tokens", systemPrompt: "System Prompt", systemPlaceholder: "Optional: enter system instructions", user: "You", assistant: "Assistant", empty: "No messages yet. Send something first.", thinking: "Generating...", error: "Request failed" },
    settings: { title: "Settings", gateway: "Gateway", version: "Version", logLevel: "Log Level", logFile: "Log File", modelPaths: "Model Paths", launchers: "Launchers", loading: "Loading settings..." },
    logs: { title: "Logs", refresh: "Refresh", empty: "No logs yet." },
  },
} as const;

const activeView = ref<ViewKey>("dashboard");
const storedLanguage = localStorage.getItem("qgateway-language") as Language | null;
const language = ref<Language>(storedLanguage === "en" || storedLanguage === "zh" ? storedLanguage : "zh");
const health = ref<Health | null>(null);
const t = computed(() => dictionaries[language.value]);
const navItems = computed(() => [
  { key: "dashboard" as const, label: t.value.nav.dashboard },
  { key: "runtime" as const, label: t.value.nav.runtime },
  { key: "models" as const, label: t.value.nav.models },
  { key: "playground" as const, label: t.value.nav.playground },
  { key: "settings" as const, label: t.value.nav.settings },
  { key: "logs" as const, label: t.value.nav.logs },
]);
const title = computed(() => t.value.nav[activeView.value]);

function toggleLanguage() { language.value = language.value === "zh" ? "en" : "zh"; localStorage.setItem("qgateway-language", language.value); }

onMounted(async () => { health.value = await getJson<Health>("/api/v1/health"); });
</script>
