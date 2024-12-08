<template>
  <div class="flex items-center justify-center bg-white min-h-screen">
    <!-- Connection Section -->
    <div class="flex flex-col justify-center w-1/2 md:w-1/3 lg:1/4">
      <!-- Input Section -->
      <div class="flex flex-col justify-center bg-gray-200 rounded-3xl py-4 px-8">
        <label class="mb-2 ml-4 text-gray-700 font-semibold">First Name</label>
        <input v-model="firstName" type="text" class="mb-4 p-2 border border-gray-300 rounded-full" />
        <label class="mb-2 ml-4 text-gray-700 font-semibold">Last Name</label>
        <input v-model="lastName" type="text" class="mb-4 p-2 border border-gray-300 rounded-full" />
        <label class="mb-2 ml-4 text-gray-700 font-semibold">Email</label>
        <input v-model="email" type="text" class="mb-4 p-2 border border-gray-300 rounded-full" />
        <label class="mb-2 ml-4 text-gray-700 font-semibold">Password</label>
        <input v-model="password" type="password" class="p-2 border border-gray-300 rounded-full" />
      </div>
      <!-- Validation Message Section -->
      <div v-if="errorMessage" class="mt-4 mb-1 px-4 py-2 bg-red-200 text-red-700 rounded">
        {{ errorMessage }}
      </div>
      <!-- Button Section -->
      <button @click="handleSignup" class="mt-4 mb-1 px-4 py-2 bg-gray-200 text-gray-700 font-bold rounded-full hover:bg-core-green hover:text-gray-50 w-full">Create Account</button>
    </div>
  </div>
</template>

<script setup>
import {ref} from 'vue';
import {useRouter} from 'vue-router';
import axios from 'axios';

const firstName = ref('');
const lastName = ref('');
const email = ref('');
const password = ref('');
const errorMessage = ref('');
const router = useRouter();

const handleSignup = async () => {
  // Validate fields
  if (!firstName.value || !lastName.value || !email.value || !password.value) {
    errorMessage.value = 'All fields are required. Please fill in the missing information.';
    return;
  }

  try {
    const response = await axios.post('http://127.0.0.1:5000/register', {
      first_name: firstName.value,
      last_name: lastName.value,
      email: email.value,
      password: password.value
    });

    if (response.status === 201) {
      router.push('/');
    } else {
      errorMessage.value = 'Registration failed. Please try again.';
    }
  } catch (error) {
    errorMessage.value = 'Registration failed. Please try again.';
  }
};
</script>