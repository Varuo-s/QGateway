<template>
  <section class="glass-card feature-card">
    <div class="section-title with-action">
      <span>{{ labels.title }}</span>
      <button class="glass-button" @click="loadLogs">{{ labels.refresh }}</button>
    </div>
    <pre class="log-viewer">{{ lines.join('\n') || labels.empty }}</pre>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { getJson } from "../api/client";

defineProps<{
  labels: {
    title: string;
    refresh: string;
    empty: string;
  };
}>();

const lines = ref<string[]>([]);

async function loadLogs() {
  const payload = await getJson<{ lines: string[] }>("/api/v1/logs?limit=200");
  lines.value = payload.lines;
}

onMounted(loadLogs);
</script>
