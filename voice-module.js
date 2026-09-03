#!/usr/bin/env node

/**
 * JARVIS - VOICE MODULE
 * Real-time multilanguage text-to-speech
 * Speaks derived truth in 7 languages
 */

const { TextToSpeechClient } = require('@google-cloud/text-to-speech');
const fs = require('fs');
const path = require('path');

const client = new TextToSpeechClient();

// Language voice mappings
const VOICE_CONFIG = {
  en: { languageCode: 'en-US', name: 'en-US-Neural2-C', ssmlGender: 'MALE' },
  es: { languageCode: 'es-ES', name: 'es-ES-Neural2-A', ssmlGender: 'MALE' },
  zh: { languageCode: 'zh-CN', name: 'zh-CN-Neural2-A', ssmlGender: 'MALE' },
  fr: { languageCode: 'fr-FR', name: 'fr-FR-Neural2-A', ssmlGender: 'MALE' },
  de: { languageCode: 'de-DE', name: 'de-DE-Neural2-C', ssmlGender: 'MALE' },
  ja: { languageCode: 'ja-JP', name: 'ja-JP-Neural2-C', ssmlGender: 'MALE' },
  ar: { languageCode: 'ar-XA', name: 'ar-XA-Neural1-A', ssmlGender: 'MALE' },
};

// Truth statements in each language
const TRUTH_STATEMENTS = {
  en: (truth) => `Atmospheric truth layer operational. Merkle root consensus achieved. K value ${truth.kValue}. Chaos stability ${truth.chaoticStability}. All satellites aligned.`,
  es: (truth) => `Capa de verdad atmosférica operacional. Consenso de raíz Merkle alcanzado. Valor K ${truth.kValue}. Estabilidad del caos ${truth.chaoticStability}. Todos los satélites alineados.`,
  zh: (truth) => `大气真相层已启动。默克尔根共识已达成。K值${truth.kValue}。混沌稳定性${truth.chaoticStability}。所有卫星对齐。`,
  fr: (truth) => `Couche de vérité atmosphérique opérationnelle. Consensus de racine Merkle atteint. Valeur K ${truth.kValue}. Stabilité du chaos ${truth.chaoticStability}. Tous les satellites alignés.`,
  de: (truth) => `Atmosphärische Wahrheitsschicht betriebsbereit. Merkle-Root-Konsens erreicht. K-Wert ${truth.kValue}. Chaos-Stabilität ${truth.chaoticStability}. Alle Satelliten ausgerichtet.`,
  ja: (truth) => `大気真実層が稼働中。マークルルートコンセンサスが達成されました。K値${truth.kValue}。混沌の安定性${truth.chaoticStability}。すべての衛星が整列しています。`,
  ar: (truth) => `طبقة الحقيقة الجوية تعمل. تم التوصل إلى إجماع جذر Merkle. قيمة K ${truth.kValue}. استقرار الفوضى ${truth.chaoticStability}. جميع الأقمار الصناعية محاذاة.`,
};

class JARVISVoiceModule {
  static async synthesizeSpeech(text, lang = 'en') {
    try {
      const voiceConfig = VOICE_CONFIG[lang];
      if (!voiceConfig) {
        throw new Error(`Unsupported language: ${lang}`);
      }

      const request = {
        input: { text: text },
        voice: {
          languageCode: voiceConfig.languageCode,
          name: voiceConfig.name,
          ssmlGender: voiceConfig.ssmlGender,
        },
        audioConfig: {
          audioEncoding: 'MP3',
          pitch: 0,
          speakingRate: 1,
        },
      };

      const [response] = await client.synthesizeSpeech(request);
      const audioContent = response.audioContent;

      return audioContent;
    } catch (err) {
      console.error(`Voice synthesis error (${lang}):`, err.message);
      return null;
    }
  }

  static async generateTruthVoice(truth, lang = 'en') {
    const statement = TRUTH_STATEMENTS[lang](truth);
    const audio = await this.synthesizeSpeech(statement, lang);
    return { statement, audio };
  }

  static async saveVoiceFile(audioContent, filename) {
    if (!audioContent) return null;
    
    const filepath = path.join(__dirname, 'voices', filename);
    
    // Create voices directory if it doesn't exist
    if (!fs.existsSync(path.join(__dirname, 'voices'))) {
      fs.mkdirSync(path.join(__dirname, 'voices'));
    }

    fs.writeFileSync(filepath, audioContent);
    return filepath;
  }

  static async generateAllLanguageVoices(truth) {
    const voiceFiles = {};

    for (const lang of Object.keys(TRUTH_STATEMENTS)) {
      try {
        console.log(`🎤 Generating voice for ${lang}...`);
        const { statement, audio } = await this.generateTruthVoice(truth, lang);
        
        if (audio) {
          const filename = `truth_${lang}_${Date.now()}.mp3`;
          const filepath = await this.saveVoiceFile(audio, filename);
          voiceFiles[lang] = {
            filename,
            statement,
            url: `/voices/${filename}`,
          };
          console.log(`✅ Voice generated: ${filename}`);
        }
      } catch (err) {
        console.error(`Error generating voice for ${lang}:`, err.message);
      }
    }

    return voiceFiles;
  }
}

module.exports = JARVISVoiceModule;
