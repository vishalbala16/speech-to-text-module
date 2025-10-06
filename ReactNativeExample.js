// React Native Integration Example
// Add this to your React Native app

import React, { useState, useEffect } from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

const SpeechToTextModule = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [transcription, setTranscription] = useState('');
  const [ws, setWs] = useState(null);

  useEffect(() => {
    // Connect to Python WebSocket server
    const websocket = new WebSocket('ws://localhost:8765');
    
    websocket.onopen = () => {
      setIsConnected(true);
      console.log('Connected to speech module');
    };
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'transcription') {
        if (data.text.includes('[WAKE]')) {
          setIsListening(true);
          setTranscription('Listening started...');
        } else if (data.text.includes('[SLEEP]')) {
          setIsListening(false);
          setTranscription('Listening stopped.');
        } else {
          setTranscription(data.text);
        }
      }
    };
    
    websocket.onclose = () => {
      setIsConnected(false);
      console.log('Disconnected from speech module');
    };
    
    setWs(websocket);
    
    return () => {
      websocket.close();
    };
  }, []);

  const startListening = () => {
    if (ws && isConnected) {
      ws.send(JSON.stringify({ action: 'start' }));
    }
  };

  const stopListening = () => {
    if (ws && isConnected) {
      ws.send(JSON.stringify({ action: 'stop' }));
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Speech-to-Text Module</Text>
      
      <Text style={styles.status}>
        Status: {isConnected ? 'Connected' : 'Disconnected'}
      </Text>
      
      <Text style={styles.status}>
        Listening: {isListening ? 'Active' : 'Inactive'}
      </Text>
      
      <View style={styles.buttons}>
        <Button 
          title="Start Listening" 
          onPress={startListening}
          disabled={!isConnected}
        />
        <Button 
          title="Stop Listening" 
          onPress={stopListening}
          disabled={!isConnected}
        />
      </View>
      
      <View style={styles.transcriptionBox}>
        <Text style={styles.transcriptionTitle}>Transcription:</Text>
        <Text style={styles.transcriptionText}>{transcription}</Text>
      </View>
      
      <Text style={styles.instructions}>
        Say "hi" to start transcription, "bye" to stop
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
  },
  status: {
    fontSize: 16,
    marginBottom: 10,
  },
  buttons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginVertical: 20,
  },
  transcriptionBox: {
    backgroundColor: 'white',
    padding: 15,
    borderRadius: 8,
    marginVertical: 20,
    minHeight: 100,
  },
  transcriptionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  transcriptionText: {
    fontSize: 16,
    color: '#333',
  },
  instructions: {
    fontSize: 14,
    textAlign: 'center',
    color: '#666',
    fontStyle: 'italic',
  },
});

export default SpeechToTextModule;