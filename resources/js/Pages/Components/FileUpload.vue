<template>
    <TransitionRoot as="template" :show="open">
        <Dialog as="div" class="relative z-10" @close="$emit('toggleFileUpload')">
            <div class="fixed inset-0"/>

            <div class="fixed inset-0 overflow-hidden">
                <div class="absolute inset-0 overflow-hidden">
                    <div class="pointer-events-none fixed inset-y-0 right-0 flex max-w-full pl-10">
                        <TransitionChild as="template"
                                         enter="transform transition ease-in-out duration-500 sm:duration-700"
                                         enter-from="translate-x-full" enter-to="translate-x-0"
                                         leave="transform transition ease-in-out duration-500 sm:duration-700"
                                         leave-from="translate-x-0" leave-to="translate-x-full">
                            <DialogPanel class="pointer-events-auto w-screen max-w-md">
                                <div class="flex h-full flex-col overflow-y-scroll bg-white py-6 shadow-xl">
                                    <div class="px-4 sm:px-6">
                                        <div class="flex items-start justify-between">
                                            <DialogTitle class="text-base font-semibold leading-6 text-gray-900">Subir
                                                Archivo
                                            </DialogTitle>
                                            <div class="ml-3 flex h-7 items-center">
                                                <button type="button"
                                                        class="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                                                        @click="$emit('toggleFileUpload')">
                                                    <span class="sr-only">Cerrar</span>
                                                    <XMarkIcon class="h-6 w-6" aria-hidden="true"/>
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="relative mt-6 flex-1 px-4 sm:px-6">
                                        <div
                                            class="mt-2 flex justify-center rounded-lg border border-dashed border-gray-900/25 px-6 py-10">
                                            <div class="text-center">
                                                <DocumentTextIcon class="mx-auto h-12 w-12 text-gray-300"
                                                                  aria-hidden="true"
                                                                  :class="{'animate-bounce': processing}"/>
                                                <div class="mt-4 flex text-sm leading-6 text-gray-600">
                                                    <label for="file-upload"
                                                           class="relative cursor-pointer rounded-md bg-white font-semibold text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-600 focus-within:ring-offset-2 hover:text-indigo-500"
                                                           v-if="!processing">
                                                        <span>Select a file </span>
                                                        <input id="file-upload" name="file-upload" type="file"
                                                               class="sr-only" @change="onFileChange"/>
                                                    </label>
                                                    <p class="pl-1" v-if="!processing">or drag and drop</p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </DialogPanel>
                        </TransitionChild>
                    </div>
                </div>
            </div>
        </Dialog>
    </TransitionRoot>
</template>

<script setup>

import {ref} from 'vue'
import {Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot} from '@headlessui/vue'
import {XMarkIcon, DocumentTextIcon} from '@heroicons/vue/24/outline'
import axios from 'axios'
import {toast} from "vue3-toastify";

const emit = defineEmits(['toggleFileUpload'])

const props = defineProps(['open'])

const processing = ref(false)

const onFileChange = (event) => {
    processing.value = true
    const file = event.target.files[0]

    const formData = new FormData()
    formData.append('file', file)
    const url = 'https://hc776dojqg.execute-api.us-east-1.amazonaws.com/dev/files'
    const config = {
        headers: {
            'Content-Type': 'text/csv'
        }
    }

    axios.post(url, formData, config).then((r) => {
        processing.value = false;
        toast.success(r.data.message);
        emit('toggleFileUpload');
    }).catch((error) => {
        processing.value = false;
        toast.error(error.message);
    })
}

</script>
