# this code is from Samhan Salahuddin 
# I have integrated it with the python tracker

from random import *

class Composer(object):
    
    def compose(self,scaleNotes,duration):
        scaleLen = len(scaleNotes)
        melody = []
        octave = 1
        cycle_length = 2**randint(0,3)
        octaveOffset = 0
        octaveMod = 0
        tension = 0
        tension_cycle = randint(1,3)
        tension_direction = 1
        tension_count = 0
        meta_tension_cycle = randint(2,5)
        meta_tension = 0
        meta_tension_direction = 1
        beat_length = 4
        beat_accumulated = 0
        total_meta_cycles = 0
        meta_cycle_max = 10
        cycle_counter = 0
        counter = 0
        previous_cycle_length = cycle_length
        # parameters to the random note offset generator
        multiplier =  randint(2,55000)
        noteCounter = randint(20,55000)
        base =  randint(1,51000)
        counter = 0

        duration_sequence = generateDurationSequence(cycle_length,beat_length,tension,tension_direction,counter,noteCounter,multiplier,base)

        while counter < duration:
            finalOffset = 0
            previousOctave = 0
            # suppress the note offset lower proportional to tension
            noteMod = 3
            if tension >= 2:
                noteMod = 2

            if tension >= 3:
                noteMod = 2

            if tension >= 5:
                noteMod = 2

            if tension >= 7:
                noteMod = 1

            if tension >=9:
                noteMod = 1

            noteOffset = generateNoteDelta(noteCounter+counter,multiplier,base) / (noteMod)
            # extend durations by even multiples every now and then
            noteDuration = duration_sequence[(noteCounter + counter) % len(duration_sequence)]
            num_cycles = 0
            
            
            #switch things up every now and then ie cycles
            if counter % cycle_length == 0 and counter != 0:
                # this makes a repetition
                melody_stringified = melody_string(melody[-min(len(melody),40):])
                compress_ratio = float(len(compress(melody_stringified))) / len(melody_stringified)

                if compress_ratio <= 0.2 :
                    noteCounter = noteCounter - cycle_length - 1
                    counter = counter + 1
                    continue

                octaveOffset = 0 

                # this actually makes the output more varied . Need to see why its required
                if randint(1,10) % 2 == 0 :
                    octaveMod =  (octaveMod + 1) % randint(2,4)

                # dont get too varied when tension has fallen
                if tension_direction == -1 and tension <= 5:
                    octaveMod = max(0,octaveMod-2)

                tension_count = tension_count + 1
                tension_ended = False

                # When cycle of rising and falling tension is complete
                if tension_count % tension_cycle == 0:

                    #Reset note generator when lowering tension from peak
                    if tension_direction == -1 :
                        # reset the random variables only after a "phrase"
                        tension_ended = True
                        multiplier =  randint(2,1000)
                        noteCounter = randint(1,5000)
                        base =  randint(1,1000)

                        if len(melody) > 1:
                            noteIn = melody.pop()
                            n = noteIn[0]
                            o = noteIn[1]
                            d = noteIn[2]
                            v = noteIn[3]
                            
                            if d <= 2:
                                d = 4

                            melody.append(("C" if randint(1,2) % 3 == 0 else n,o,d, v))

                        melody.append(("S",finalOctaveOffset,8, 25 + 20*int(tension/9) + randint(4,8)))

                    # Restart tension cycle
                    tension_count = 0
                    tension_direction = tension_direction * -1
                    # This adds long range structure . Starts and ends slow. Can increase randomn upper range if
                    # output is too dull.
                    tension_cycle = meta_tension + randint(1,3)
                    meta_tension = meta_tension + randint(1,2)

                    # same thing as tension but meta
                    if meta_tension_cycle % meta_tension == 0:
                        meta_tension = 0
                        meta_tension_direction = meta_tension_direction * -1
                        meta_tension_cycle = randint(2,5)
                        total_meta_cycles = total_meta_cycles + 1
                        octaveMod =  (octaveMod + 1) % 3

                    if total_meta_cycles == meta_cycle_max:
                        if len(melody) > 1:
                            noteIn = melody.pop()
                            n = noteIn[0]
                            o = noteIn[1]
                            d = noteIn[2]
                            v = noteIn[3]
                            melody.append((n,o,8, v))
                        return melody
                    


                meta_term = meta_tension if meta_tension_direction == 1 else -1*meta_tension

                # this is a hack to force tension back down. Need to see if it can be avoided
                fraction = tension_count / tension_cycle

                tension = (meta_term + (tension + tension_direction*randint(1,2) )) % randint(6,8)
               
                if fraction >= 0.75 and tension_direction == -1:
                    tension = randint(1,3) 
                elif (tension_count + 1) % tension_cycle == 0:
                    tension = randint(1,2)

                # generate note lengths based on cycle length , beat length and tension . beat length not used
                # need to fix to accomodate both odd and even rhythms
                duration_sequence = generateDurationSequence(cycle_length,beat_length,tension,tension_direction,counter,noteCounter,multiplier,base)
                
                # Every now and then make the phrases longer or shorter based on the tension

                melody_stringified = melody_string(melody[-len(melody):])
                compress_ratio = float(len(compress(melody_stringified))) / len(melody_stringified)
                

                if compress_ratio >= 0.2:
                   prev_cyc = cycle_length
                   cycle_length = 2 + 2**randint(1,2) 
                   if tension >= 4:
                        cycle_length = 2**randint(2,2)
                   if tension >= 6:
                        cycle_length = 2**randint(2,3) 
                   if tension >= 7:
                        cycle_length = 2**randint(1,2) 

                   octaveOffset = randint(0,1)
                   tension = 0

                   if prev_cyc > 4:
                       duration_sequence = generateDurationSequence(cycle_length,beat_length,tension,tension_direction,counter,noteCounter,multiplier,base)

                counter = counter + 1
                continue

            finalOctaveOffset = 0 if octaveMod == 0 else (octave + octaveOffset) % octaveMod
            finalOctaveOffset = finalOctaveOffset + 2
            previousOctave = finalOctaveOffset
            previousOffset = finalOffset

            chromatic = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
            finalOffset = chromatic.index(scaleNotes[noteOffset % scaleLen]) + 12*finalOctaveOffset

            if finalOffset / 12 >= 6:
                finalOctaveOffset = 5
            melody.append((scaleNotes[noteOffset % scaleLen],finalOctaveOffset,noteDuration, 30 + 20*int(tension/9) + randint(4,8) + meta_tension))
            counter = counter + 1
            previousOctave = finalOffset / 12
           

        return melody


def melody_string(notes):
    noteList = [note[0]+str(note[2]) for note in notes]
    return ''.join(noteList)

def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n /= b
    return digits[::-1]

def sumOfDigits(num):
    result = 0
    for digit in num:
        result = result + int(digit)

    return result

def generateNoteDelta(counter,base,multiplier):
    return sumOfDigits(numberToBase((counter * multiplier),base))

def generateDurationSequence(cycle_length,beat_length,tension,tension_direction,counter,noteCounter,multiplier,base):
    base_duration = 2
    # longer notes for lower tension and vice versa
    fractal_seq =  [generateNoteDelta(noteCounter+counter + x,multiplier,base)  for x in range(0,9)]
    fractal_seq =  [round(float(max(fractal_seq))/float(x))  for x in fractal_seq]
    ascending_rhythm_powers =  [randint(2,3),randint(2,3),randint(2,3),randint(3,4),randint(3,4),randint(2,3),randint(2,3),randint(1,2),randint(1,2)]
  
    max_power = int(ascending_rhythm_powers[tension] if randint(1,2) % 2 == 0 else fractal_seq[tension]) 
    uniform_beats = [2*randint(1,max_power) for x in range(0,cycle_length)]
    target = 8

    if tension >= 0 and tension <= 2:
        target = 8*randint(1,3)
    elif tension <= 4:
        target = 8 *randint (1,2)
    else:
        target = 4*randint(1,3)

    counter = 0

    # this is what keeps it on beat. keep generating random note lengths until you get something that
    # lines up with the beat. On failure try worse and worse alignments.
    while True:
        uniform_beats = [2*randint(1,max_power) for x in range(0,cycle_length)]
        if counter % 5000 == 0:
            target = target/2
        sum_beats = sum(uniform_beats)
        if  sum_beats % target == 0:
            break

    return uniform_beats

## LZW Compression Implementation Used To See If Output Is Repetitive
## Source : Rosetta Code
def compress(uncompressed):
    dict_size = 256
    dictionary = dict((chr(i), i) for i in xrange(dict_size))
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
    if w:
        result.append(dictionary[w])
    return result


majorScaleNotes = ['C','D','E','F','G','A']
pentatonic = ['C','D','E','G','A']
bluesScaleNotes = ['C','D#','F','F#','A#']
arabScaleNotes = ['C','C#','E','F','G','G#']
spanish = ['C', 'C#',  'E'  ,'F'  ,'G' , 'G#' ,'A#']

mozart = Composer()
testMelody = mozart.compose(spanish,10)
print testMelody