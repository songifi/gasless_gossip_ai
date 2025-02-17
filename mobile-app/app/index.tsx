import { Button, StyleSheet, Text, TouchableOpacity, View } from 'react-native'
import React from 'react'
import OnboardingScreen from "./screens/onboarding/OnboardingScreen"
import { router } from 'expo-router'

export default function index() {
  return (
    <View style={{flex:1, justifyContent: 'center', alignItems: 'center'}}>
      <OnboardingScreen />
      <TouchableOpacity>
      <Button title='Home' onPress={() => router.push('/(drawer)/(tabs)')} />
      </TouchableOpacity>
    </View>
  )
}

const styles = StyleSheet.create({})