<template>
  <div class="view-stack">
    <section class="glass-card feature-card models-header">
      <div>
        <div class="section-title">{{ labels.title }}</div>
        <p class="section-subtitle">{{ labels.subtitle }}</p>
      </div>
      <div class="top-actions">
        <button class="glass-button" @click="loadAll">{{ labels.refresh }}</button>
        <button class="glass-button" @click="saveRuntime">{{ labels.save }}</button>
        <button class="glass-button" @click="startRuntime">{{ labels.start }}</button>
        <button class="glass-button danger" @click="stopRuntime">{{ labels.stop }}</button>
      </div>
    </section>

    <section class="metric-grid three-metrics">
      <article class="glass-card metric-card compact"><span class="card-label">{{ labels.state }}</span><strong>{{ stateLabel }}</strong></article>
      <article class="glass-card metric-card compact"><span class="card-label">{{ labels.provider }}</span><strong>{{ status?.provider ?? labels.unknown }}</strong></article>
      <article class="glass-card metric-card compact"><span class="card-label">{{ labels.pid }}</span><strong>{{ status?.pid ?? '--' }}</strong></article>
    </section>

    <section class="runtime-editor-grid">
      <article class="glass-card feature-card parameter-panel">
        <div class="section-title">{{ labels.runtimeConfig }}</div>
        <label><span>{{ labels.model }}</span><select v-model="form.model_path"><option v-for="model in models" :key="model.path" :value="model.path">{{ model.name }}</option></select></label>
        <label><span>{{ labels.alias }}</span><input v-model="form.alias" /></label>
        <label><span>{{ labels.host }}</span><select v-model="form.host"><option value="127.0.0.1">127.0.0.1 · {{ labels.localOnly }}</option><option value="0.0.0.0">0.0.0.0 · {{ labels.lan }}</option></select></label>
        <label><span>{{ labels.port }}</span><input v-model.number="form.port" type="number" min="1" max="65535" /></label>
        <label><span>{{ labels.gpuLayers }}</span><input v-model="form.gpu_layers" /></label>
        <label><span>{{ labels.context }}</span><input v-model.number="form.context_size" type="number" min="512" /></label>
        <label><span>{{ labels.flashAttention }}</span><select v-model="form.flash_attention"><option value="auto">auto</option><option value="on">on</option><option value="off">off</option></select></label>
        <label><span>{{ labels.reasoning }}</span><select v-model="form.reasoning"><option value="off">off</option><option value="on">on</option><option value="auto">auto</option></select></label>
        <label><span>{{ labels.reasoningFormat }}</span><select v-model="form.reasoning_format"><option value="none">none</option><option value="deepseek">deepseek</option><option value="qwen">qwen</option></select></label>
        <label><span>{{ labels.logColors }}</span><select v-model="form.log_colors"><option value="off">off</option><option value="on">on</option></select></label>
        <label><span>{{ labels.extraArgs }}</span><input v-model="extraArgsText" placeholder="--no-webui" /></label>
      </article>

      <article class="glass-card feature-card">
        <div class="section-title">{{ labels.command }}</div>
        <pre class="config-preview">{{ status?.command.join(' ') }}</pre>
        <div class="glass-table settings-table" v-if="status">
          <div class="glass-row"><span>{{ labels.endpoint }}</span><strong>{{ status.host }}:{{ status.port }}</strong></div>
          <div class="glass-row"><span>{{ labels.executable }}</span><strong>{{ status.executable }} · {{ status.executable_exists ? labels.exists : labels.missing }}</strong></div>
          <div class="glass-row"><span>{{ labels.model }}</span><strong>{{ status.model_path }} · {{ status.model_exists ? labels.exists : labels.missing }}</strong></div>
          <div v-if="status.error" class="glass-row error-row"><span>{{ labels.error }}</span><strong>{{ status.error }}</strong></div>
        </div>
      </article>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { getJson } from "../api/client";

type RuntimeStatus = { state: "stopped" | "running" | "error"; provider: string; executable: string; executable_exists: boolean; model_path: string; model_exists: boolean; host: string; port: number; pid: number | null; command: string[]; error: string | null };
type ModelItem = { name: string; path: string };
type RuntimeForm = { model_path: string; alias: string; host: string; port: number; gpu_layers: string; context_size: number; flash_attention: string; reasoning: string; reasoning_format: string; log_colors: string; extra_args: string[] };

const props = defineProps<{ labels: Record<string, string> }>();
const status = ref<RuntimeStatus | null>(null);
const models = ref<ModelItem[]>([]);
const extraArgsText = ref("");
const form = reactive<RuntimeForm>({ model_path: "", alias: "", host: "127.0.0.1", port: 8999, gpu_layers: "all", context_size: 16384, flash_attention: "auto", reasoning: "off", reasoning_format: "none", log_colors: "off", extra_args: [] });

const stateLabel = computed(() => {
  if (!status.value) return props.labels.unknown;
  if (status.value.state === "running") return props.labels.running;
  if (status.value.state === "stopped") return props.labels.stopped;
  return "Error";
});

function applyRuntime(runtime: Partial<RuntimeForm>) {
  Object.assign(form, runtime);
  extraArgsText.value = (runtime.extra_args || []).join(" ");
}

async function loadSettings() {
  const payload = await getJson<{ runtime: RuntimeForm }>("/api/v1/settings");
  applyRuntime(payload.runtime);
}
async function loadModels() { const payload = await getJson<{ models: ModelItem[] }>("/api/v1/models/scan"); models.value = payload.models; }
async function loadStatus() { status.value = await getJson<RuntimeStatus>("/api/v1/runtime/status"); }
async function loadAll() { await Promise.all([loadSettings(), loadModels(), loadStatus()]); }

function payload() { return { ...form, extra_args: extraArgsText.value.trim() ? extraArgsText.value.trim().split(/\s+/) : [] }; }

async function saveRuntime() {
  const response = await fetch("/api/v1/settings/runtime", { method: "PUT", headers: { Accept: "application/json", "Content-Type": "application/json" }, body: JSON.stringify(payload()) });
  if (!response.ok) throw new Error(`Request failed: ${response.status}`);
  const result = await response.json() as { runtime: RuntimeForm; status: RuntimeStatus };
  applyRuntime(result.runtime);
  status.value = result.status;
}
async function postRuntime(path: string) { const response = await fetch(path, { method: "POST", headers: { Accept: "application/json", "Content-Type": "application/json" }, body: JSON.stringify(payload()) }); if (!response.ok) throw new Error(`Request failed: ${response.status}`); status.value = await response.json() as RuntimeStatus; }
async function startRuntime() { await saveRuntime(); await postRuntime("/api/v1/runtime/start"); }
async function stopRuntime() { await postRuntime("/api/v1/runtime/stop"); }

onMounted(loadAll);
</script>
