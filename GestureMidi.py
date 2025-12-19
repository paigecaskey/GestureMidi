import cv2
import mediapipe as mp
import mido
import time

class GestureDJ:
    '''
    A hand gesture controlled DJ system using MIDI signals.
    Uses MediaPipe for hand tracking and mido for MIDI communication.
    Requirements:
    pip install opencv-python mediapipe mido python-rtmidi
    1. Set up a virtual MIDI port (loopMIDI for Windows, IAC Driver for Mac, ALSA for Linux).
    2. Configure your DJ software to receive MIDI from the virtual port.
    3. Use MIDI Learn in your DJ software to map controls.
    Controls:
    - ✊ Fist: No action
    - 🖐 Open hand with thumb out: Play
    - 🤙 Thumb + pinky: Control Volume
    - 🤘 Pinky only: Control Low EQ
    - ☝️ Index finger only: Control Mid EQ
    - ✌️ Index + middle fingers: Control High EQ
    Software will display current actions on left corner screen.
    DJ software:
    - Mixxx (https://mixxx.org/) is an open-source option that supports MIDI mapping.
    '''
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.draw = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)

        ports = mido.get_output_names()
        if not ports:
            raise RuntimeError("No MIDI ports found")
        self.midi = mido.open_output(ports[0])
        print("Connected MIDI:", ports[0])

        self.last_play = {"Left": 0, "Right": 0}

    # ---------- MIDI ----------
    def send_cc(self, cc, value):
        value = max(0, min(127, int(value)))
        self.midi.send(mido.Message("control_change", control=cc, value=value))

    def send_play(self, note):
        self.midi.send(mido.Message("note_on", note=note, velocity=127))

    # ---------- Helpers ----------
    def fingers_up(self, lm):
        tips = [8, 12, 16, 20]
        return [lm[i].y < lm[i-2].y for i in tips]

    def thumb_out(self, lm, hand):
        return lm[4].x < lm[3].x if hand == "Right" else lm[4].x > lm[3].x

    def vertical_value(self, lm):
        return int((1 - lm[0].y) * 127)

    # ---------- Gesture Logic ----------
    def process_hand(self, lm, hand):
        fingers = self.fingers_up(lm)
        thumb = self.thumb_out(lm, hand)
        height = self.vertical_value(lm)

        # Deck routing
        deck_offset = 0 if hand == "Left" else 10

        label = "NULL"

        # ✊ NULL — fist
        if sum(fingers) == 0:
            return label

        # 🖐 PLAY
        if sum(fingers) == 4 and thumb:
            now = time.time()
            if now - self.last_play[hand] > 0.6:
                self.send_play(60 + deck_offset)
                self.last_play[hand] = now
            return "PLAY"

        # 🤙 VOLUME (thumb + pinky)
        if thumb and fingers == [False, False, False, True]:
            self.send_cc(1 + deck_offset, height)
            return "VOLUME"

        # 🤘 LOW EQ (pinky only)
        if fingers == [False, False, False, True] and not thumb:
            self.send_cc(2 + deck_offset, height)
            return "LOW EQ"

        # ☝️ MID EQ
        if fingers == [True, False, False, False]:
            self.send_cc(3 + deck_offset, height)
            return "MID EQ"

        # ✌️ HIGH EQ
        if fingers == [True, True, False, False]:
            self.send_cc(4 + deck_offset, height)
            return "HIGH EQ"

        return label

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = self.hands.process(rgb)

            left_label, right_label = "—", "—"

            if res.multi_hand_landmarks:
                for lm, h in zip(res.multi_hand_landmarks, res.multi_handedness):
                    self.draw.draw_landmarks(frame, lm, self.mp_hands.HAND_CONNECTIONS)
                    hand = h.classification[0].label
                    label = self.process_hand(lm.landmark, hand)
                    if hand == "Left":
                        left_label = label
                    else:
                        right_label = label

            cv2.putText(frame, f"L: {left_label}", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
            cv2.putText(frame, f"R: {right_label}", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3)

            cv2.imshow("Gesture DJ Controller", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    GestureDJ().run()




