<template>
  <div class="view-stack">
    <section class="glass-card feature-card models-header">
      <div>
        <div class="section-title">{{ labels.title }}</div>
        <p class="section-subtitle">{{ labels.subtitle }}</p>
      </div>
      <button class="glass-button" @click="loadConfigs">{{ labels.refresh }}</button>
    </section>

    <section class="client-grid">
      <article v-for="config in configs" :key="config.id" class="glass-card feature-card client-card">
        <div class="client-card-header">
          <div>
            <div class="section-title">{{ config.name }}</div>
            <p class="section-subtitle">{{ config.filename }} · {{ config.format.toUpperCase() }}</p>
          </div>
          <div class="top-actions">
            <button class="glass-button" @click="copyConfig(config.content)">{{ labels.copy }}</button>
            <button class="glass-button" @click="downloadConfig(config)">{{ labels.download }}</button>
          </div>
        </div>
        <pre class="config-preview">{{ config.content }}</pre>
      </article>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { getJson } from "../api/client";

type ClientConfig = {
  id: string;
  name: string;
  format: "json" | "toml" | "yaml";
  filename: string;
  content: string;
};

defineProps<{
  labels: {
    title: string;
    subtitle: string;
    refresh: string;
    copy: string;
    download: string;
  };
}>();

const configs = ref<ClientConfig[]>([]);

async function loadConfigs() {
  const payload = await getJson<{ configs: ClientConfig[] }>("/api/v1/clients/configs");
  configs.value = payload.configs;
}

async function copyConfig(content: string) {
  await navigator.clipboard.writeText(content);
}

function downloadConfig(config: ClientConfig) {
  const blob = new Blob([config.content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = config.filename;
  link.click();
  URL.revokeObjectURL(url);
}

onMounted(loadConfigs);
</script>
