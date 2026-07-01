<template>
  <div class="playground-layout">
    <section class="glass-card feature-card chat-panel">
      <div class="models-header">
        <div>
          <div class="section-title">{{ labels.title }}</div>
          <p class="section-subtitle">{{ labels.subtitle }}</p>
        </div>
        <button class="glass-button" @click="clearMessages">{{ labels.clear }}</button>
      </div>

      <div class="message-list">
        <div v-if="messages.length === 0" class="empty-state">{{ labels.empty }}</div>
        <article v-for="message in messages" :key="message.id" class="message-bubble" :class="message.role">
          <span>{{ message.role === 'user' ? labels.user : labels.assistant }}</span>
          <p>{{ message.content }}</p>
        </article>
        <article v-if="loading" class="message-bubble assistant">
          <span>{{ labels.assistant }}</span>
          <p>{{ labels.thinking }}</p>
        </article>
        <article v-if="error" class="message-bubble error-message">
          <span>{{ labels.error }}</span>
          <p>{{ error }}</p>
        </article>
      </div>

      <div class="composer">
        <textarea v-model="draft" :placeholder="labels.placeholder" @keydown.ctrl.enter.prevent="sendMessage"></textarea>
        <button class="glass-button send-button" :disabled="loading || !draft.trim()" @click="sendMessage">{{ labels.send }}</button>
      </div>
    </section>

    <aside class="glass-card feature-card parameter-panel">
      <div class="section-title">{{ labels.parameters }}</div>
      <label>
        <span>{{ labels.systemPrompt }}</span>
        <textarea v-model="systemPrompt" class="small-textarea" :placeholder="labels.systemPlaceholder"></textarea>
      </label>
      <label>
        <span>{{ labels.temperature }}: {{ temperature }}</span>
        <input v-model.number="temperature" type="range" min="0" max="2" step="0.1" />
      </label>
      <label>
        <span>{{ labels.topP }}: {{ topP }}</span>
        <input v-model.number="topP" type="range" min="0.1" max="1" step="0.05" />
      </label>
      <label>
        <span>{{ labels.maxTokens }}</span>
        <input v-model.number="maxTokens" type="number" min="16" max="4096" />
      </label>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

defineProps<{
  labels: {
    title: string; subtitle: string; placeholder: string; send: string; clear: string; parameters: string; temperature: string; topP: string; maxTokens: string; systemPrompt: string; systemPlaceholder: string; user: string; assistant: string; empty: string; thinking: string; error: string;
  };
}>();

const messages = ref<ChatMessage[]>([]);
const draft = ref("");
const systemPrompt = ref("");
const temperature = ref(0.7);
const topP = ref(0.95);
const maxTokens = ref(512);
const loading = ref(false);
const error = ref<string | null>(null);

function makeId(prefix: string) {
  return `${prefix}_${Date.now()}_${Math.random().toString(16).slice(2)}`;
}

function clearMessages() {
  messages.value = [];
  error.value = null;
}

async function sendMessage() {
  const content = draft.value.trim();
  if (!content || loading.value) {
    return;
  }

  messages.value.push({ id: makeId("user"), role: "user", content });
  draft.value = "";
  loading.value = true;
  error.value = null;

  try {
    const response = await fetch("/v1/responses", {
      method: "POST",
      headers: { Accept: "application/json", "Content-Type": "application/json" },
      body: JSON.stringify({
        input: content,
        instructions: systemPrompt.value.trim() || undefined,
        temperature: temperature.value,
        top_p: topP.value,
        max_output_tokens: maxTokens.value,
      }),
    });
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail || `HTTP ${response.status}`);
    }
    const payload = await response.json() as { output_text?: string };
    messages.value.push({ id: makeId("assistant"), role: "assistant", content: payload.output_text || "" });
  } catch (exc) {
    error.value = exc instanceof Error ? exc.message : String(exc);
  } finally {
    loading.value = false;
  }
}
</script>
