<script setup lang="ts">
</script>

<template>
    <section id="features" class="py-20 bg-muted/30">
        <div class="container mx-auto px-4">
            <div class="text-center mb-16">
                <h2 class="text-4xl font-bold mb-4">Powerful Features</h2>
                <p class="text-xl text-muted-foreground max-w-2xl mx-auto">
                    Everything you need to stay organized and productive
                </p>
            </div>

            <div class="grid md:grid-cols-3 gap-8">
                <!-- Feature 1 -->
                <div class="bg-card rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
                    <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                        <svg class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-semibold mb-2">Task Management</h3>
                    <p class="text-muted-foreground">
                        Create, organize, and track your tasks with ease. Set priorities, due dates, and reminders.
                    </p>
                </div>

                <!-- Feature 2 -->
                <div class="bg-card rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
                    <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                        <svg class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-semibold mb-2">Time Tracking</h3>
                    <p class="text-muted-foreground">
                        Monitor how much time you spend on each task. Gain insights into your productivity patterns.
                    </p>
                </div>

                <!-- Feature 3 -->
                <div class="bg-card rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
                    <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                        <svg class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-semibold mb-2">Real-time Sync</h3>
                    <p class="text-muted-foreground">
                        Access your tasks from any device. Changes sync instantly across all your devices.
                    </p>
                </div>
            </div>
        </div>
    </section>
</template>