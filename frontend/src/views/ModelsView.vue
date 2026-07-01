<template>
  <div class="view-stack">
    <section class="glass-card feature-card models-header">
      <div>
        <div class="section-title">{{ labels.title }}</div>
        <p class="section-subtitle">{{ labels.subtitle }}</p>
      </div>
      <button class="glass-button" @click="loadModels">{{ labels.rescan }}</button>
    </section>

    <section class="metric-grid two-metrics">
      <article class="glass-card metric-card compact">
        <span class="card-label">{{ labels.count }}</span>
        <strong>{{ payload?.count ?? 0 }}</strong>
      </article>
      <article class="glass-card metric-card compact">
        <span class="card-label">{{ labels.scanTime }}</span>
        <strong class="time-value">{{ formattedScanTime }}</strong>
      </article>
    </section>

    <section class="glass-card feature-card">
      <div v-if="loading" class="loading-text">{{ labels.loading }}</div>
      <div v-else-if="!payload || payload.models.length === 0" class="empty-state">{{ labels.empty }}</div>
      <div v-else class="model-list">
        <article v-for="model in payload.models" :key="model.path" class="model-item">
          <div class="model-main">
            <strong>{{ model.name }}</strong>
            <span>{{ model.relative_path }}</span>
          </div>
          <div class="model-meta">
            <span>{{ labels.size }}: {{ model.size_label }}</span>
            <span>{{ labels.format }}: {{ model.format }}</span>
            <span>{{ labels.quantization }}: {{ model.quantization ?? labels.unknown }}</span>
          </div>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { getJson } from "../api/client";

type ModelItem = {
  name: string;
  size_bytes: number;
  size_label: string;
  path: string;
  relative_path: string;
  format: string;
  quantization: string | null;
  modified_at: string;
};

type ModelsPayload = {
  count: number;
  scan_time: string;
  models: ModelItem[];
};

const props = defineProps<{
  labels: {
    title: string;
    subtitle: string;
    rescan: string;
    empty: string;
    count: string;
    scanTime: string;
    name: string;
    size: string;
    format: string;
    quantization: string;
    path: string;
    unknown: string;
    loading: string;
  };
}>();

const payload = ref<ModelsPayload | null>(null);
const loading = ref(false);

const formattedScanTime = computed(() => {
  if (!payload.value?.scan_time) {
    return "--";
  }
  return new Date(payload.value.scan_time).toLocaleString();
});

async function loadModels() {
  loading.value = true;
  try {
    payload.value = await getJson<ModelsPayload>("/api/v1/models/scan");
  } finally {
    loading.value = false;
  }
}

void props;
onMounted(loadModels);
</script>
