<template>
  <el-card>
    <template #header>Settings</template>
    <el-skeleton v-if="!settings" :rows="6" animated />
    <el-descriptions v-else :column="1" border>
      <el-descriptions-item label="Gateway">{{ settings.gateway.host }}:{{ settings.gateway.port }}</el-descriptions-item>
      <el-descriptions-item label="Version">{{ settings.gateway.version }}</el-descriptions-item>
      <el-descriptions-item label="Log Level">{{ settings.logs.level }}</el-descriptions-item>
      <el-descriptions-item label="Log File">{{ settings.logs.file }}</el-descriptions-item>
      <el-descriptions-item label="Model Paths">{{ settings.models.scan_paths.join(', ') }}</el-descriptions-item>
      <el-descriptions-item label="Launchers">{{ settings.launcher.executables.join(', ') }}</el-descriptions-item>
    </el-descriptions>
  </el-card>
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

const settings = ref<Settings | null>(null);

onMounted(async () => {
  settings.value = await getJson<Settings>("/api/v1/settings");
});
</script>
