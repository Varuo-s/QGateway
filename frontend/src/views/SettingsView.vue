<template>
  <section class="glass-card feature-card">
    <div class="section-title">{{ labels.title }}</div>
    <div v-if="!settings" class="loading-text">{{ labels.loading }}</div>
    <div v-else class="glass-table settings-table">
      <div class="glass-row"><span>{{ labels.gateway }}</span><strong>{{ settings.gateway.host }}:{{ settings.gateway.port }}</strong></div>
      <div class="glass-row"><span>{{ labels.version }}</span><strong>{{ settings.gateway.version }}</strong></div>
      <div class="glass-row"><span>{{ labels.logLevel }}</span><strong>{{ settings.logs.level }}</strong></div>
      <div class="glass-row"><span>{{ labels.logFile }}</span><strong>{{ settings.logs.file }}</strong></div>
      <div class="glass-row"><span>{{ labels.modelPaths }}</span><strong>{{ settings.models.scan_paths.join(', ') }}</strong></div>
      <div class="glass-row"><span>{{ labels.launchers }}</span><strong>{{ settings.launcher.executables.join(', ') }}</strong></div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { getJson } from "../api/client";

type Settings = {
  gateway: { host: string; port: number; version: string };
  logs: { level: string; file: string };
  models: { scan_paths: string[] };
  launcher: { executables: string[] };
};

defineProps<{
  labels: {
    title: string;
    gateway: string;
    version: string;
    logLevel: string;
    logFile: string;
    modelPaths: string;
    launchers: string;
    loading: string;
  };
}>();

const settings = ref<Settings | null>(null);

onMounted(async () => {
  settings.value = await getJson<Settings>("/api/v1/settings");
});
</script>
