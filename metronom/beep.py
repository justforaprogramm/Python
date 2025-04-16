from winsound import Beep
import time

class PlayBeep:
    def __init__(self, frequency=1000, duration=100):
        self.frequency = frequency
        self.duration = duration

    def play_pattern(self, low_freq=500, high_freq=1500, low_duration=500, high_duration=500, interval=0.3):
        try:
            while True:
                # One low beep
                Beep(low_freq, low_duration)
                time.sleep(interval)
                # Three high beeps
                for _ in range(3):
                    Beep(high_freq, high_duration)
                    time.sleep(interval)
        except KeyboardInterrupt:
            print("\nPattern stopped by user.")

def main():
    beep = PlayBeep()
    beep.play_pattern(low_freq=500, high_freq=1500,)

if __name__ == '__main__':
    main()