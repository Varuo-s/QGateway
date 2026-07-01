<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>Logs</span>
        <el-button size="small" @click="loadLogs">Refresh</el-button>
      </div>
    </template>
    <pre class="log-viewer">{{ lines.join('\n') || 'No logs yet.' }}</pre>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { getJson } from "../api/client";

const lines = ref<string[]>([]);

async function loadLogs() {
  const payload = await getJson<{ lines: string[] }>("/api/v1/logs?limit=200");
  lines.value = payload.lines;
}

onMounted(loadLogs);
</script>
