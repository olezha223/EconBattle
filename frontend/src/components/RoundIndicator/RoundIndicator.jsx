import styles from './RoundIndicator.module.css';

export default function RoundIndicator({ total, current, results }) {
  return (
    <div className={styles.container}>
      {Array.from({ length: total }).map((_, index) => (
        <div
          key={index}
          className={`${styles.dot} ${
            results[index] === 'win' ? styles.win :
            results[index] === 'lose' ? styles.lose :
            results[index] === 'draw' ? styles.draw : 
            index === current - 1 ? styles.current : ''
          }`}
        >
          {index + 1}
        </div>
      ))}
    </div>
  );
}