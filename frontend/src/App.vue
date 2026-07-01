<template>
  <el-container class="app-shell">
    <el-aside width="232px" class="sidebar">
      <div class="brand">
        <div class="brand-mark">Q</div>
        <div>
          <h1>QGateway</h1>
          <span>Open Source AI Runtime</span>
        </div>
      </div>
      <el-menu :default-active="activeView" class="nav" @select="activeView = $event">
        <el-menu-item index="dashboard">Dashboard</el-menu-item>
        <el-menu-item index="settings">Settings</el-menu-item>
        <el-menu-item index="logs">Logs</el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="topbar">
        <div>
          <strong>{{ title }}</strong>
          <span>Alpha 0.1</span>
        </div>
        <el-tag :type="health?.status === 'ok' ? 'success' : 'warning'">
          {{ health?.status ?? 'checking' }}
        </el-tag>
      </el-header>
      <el-main class="content">
        <DashboardView v-if="activeView === 'dashboard'" :health="health" />
        <SettingsView v-else-if="activeView === 'settings'" />
        <LogsView v-else />
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

type Health = {
  status: string;
  service: string;
  version: string;
  runtime: string;
  uptime_seconds: number;
};

const activeView = ref("dashboard");
const health = ref<Health | null>(null);
const title = computed(() => activeView.value.charAt(0).toUpperCase() + activeView.value.slice(1));

onMounted(async () => {
  health.value = await getJson<Health>("/api/v1/health");
});
</script>
