import { CircularProgressbar, buildStyles } from 'react-circular-progressbar'
import 'react-circular-progressbar/dist/styles.css'

export default function ScoreGauge({ score, label, type = 'plagiarism' }) {
  // Determine color based on score and type
  const getColor = () => {
    if (type === 'plagiarism') {
      if (score > 50) return '#ef4444' // red
      if (score > 25) return '#f97316' // orange
      return '#22c55e' // green
    } else {
      // AI detection
      if (score > 70) return '#ef4444' // red
      if (score > 40) return '#f97316' // orange
      return '#22c55e' // green
    }
  }

  const getLevel = () => {
    if (type === 'plagiarism') {
      if (score > 50) return 'ÉLEVÉ'
      if (score > 25) return 'MOYEN'
      return 'FAIBLE'
    } else {
      if (score > 70) return 'DÉTECTÉ'
      if (score > 40) return 'POSSIBLE'
      return 'PEU PROBABLE'
    }
  }

  return (
    <div className="flex flex-col items-center space-y-3">
      <div className="w-32 h-32">
        <CircularProgressbar
          value={score}
          text={`${Math.round(score)}%`}
          styles={buildStyles({
            pathColor: getColor(),
            textColor: getColor(),
            trailColor: '#e5e7eb',
            textSize: '24px',
          })}
        />
      </div>
      <div className="text-center">
        <h3 className="font-semibold text-lg text-gray-900">{label}</h3>
        <p className="text-sm font-medium" style={{ color: getColor() }}>
          {getLevel()}
        </p>
      </div>
    </div>
  )
}
