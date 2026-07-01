<template>
  <div class="view-stack">
    <el-row :gutter="16">
      <el-col :span="8">
        <el-card>
          <template #header>Backend</template>
          <p class="metric">{{ health?.status ?? 'checking' }}</p>
          <span class="muted">{{ health?.service ?? 'QGateway' }}</span>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>Runtime</template>
          <p class="metric">{{ health?.runtime ?? 'unknown' }}</p>
          <span class="muted">Uptime {{ health?.uptime_seconds ?? 0 }}s</span>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>Version</template>
          <p class="metric">{{ health?.version ?? 'alpha-0.1' }}</p>
          <span class="muted">Milestone 1</span>
        </el-card>
      </el-col>
    </el-row>

    <el-card>
      <template #header>Alpha 0.1 Scope</template>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="Health API">Ready</el-descriptions-item>
        <el-descriptions-item label="Settings">Read-only</el-descriptions-item>
        <el-descriptions-item label="Logs">Recent file log viewer</el-descriptions-item>
        <el-descriptions-item label="Launcher">Detection only</el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  health: null | {
    status: string;
    service: string;
    version: string;
    runtime: string;
    uptime_seconds: number;
  };
}>();
</script>
