# Automated Composition with Pitch Set Theory in Web Audio

For this lab, I implemented an automated composition system based on **pitch set theory** using **JavaScript** and the **Web Audio API**. Out of the three techniques we discussed in class—Markov chain learning, cellular automata, and pitch set theory I chose pitch set theory because it offered a compelling mix of musical structure and creative freedom. It also felt like a good way to better understand how formal musical operations can become the basis of an actual generative tool.

At a high level, my system begins with a user-provided **pitch class sequence**, then repeatedly transforms it using the three core operations required for this lab: **transpose**, **inverse**, and **retrograde**. The transformed material is then mapped to audible notes and played back in the browser. Although the underlying rules are simple, the resulting compositions are surprisingly varied while still sounding related to the original musical idea.

## Why I chose pitch set theory

One of the reasons I chose this approach is that it sits in an interesting middle ground between randomness and control. A purely random note generator can produce sound, but it often lacks identity or coherence. On the other hand, pitch set theory starts with a fixed set of relationships and then explores that material through structured transformations. This means the output can change each time the piece is generated, but it still retains a recognizable musical logic.

I also liked that this technique makes the connection between music theory and code especially visible. Each transformation has a clear conceptual meaning and a straightforward computational implementation. That made it a satisfying system to build from scratch, because every line of code corresponded to a musical idea rather than just a technical step.

## Pitch classes and transformations

The basis of the project is the idea of a **pitch class**, which represents a note independent of octave. Instead of thinking in terms of specific frequencies or keyboard positions, pitch classes reduce notes to integers from **0 to 11**, where:

- 0 = C  
- 1 = C♯/D♭  
- 2 = D  
- 3 = D♯/E♭  
- 4 = E  
- 5 = F  
- 6 = F♯/G♭  
- 7 = G  
- 8 = G♯/A♭  
- 9 = A  
- 10 = A♯/B♭  
- 11 = B  

Using pitch classes makes it possible to talk about interval structure in a compact way. My program takes an initial pitch class sequence such as `[0, 2, 4, 7]` and applies the following operations:

### Transpose

Transposition shifts every pitch class in the sequence by the same amount modulo 12. For example, transposing `[0, 2, 4, 7]` up by 3 produces `[3, 5, 7, 10]`. In musical terms, this preserves the interval relationships between notes while moving the material into a different pitch area.

### Inverse

Inversion reflects the notes around a reference pitch class. In my implementation, I used the first note of the sequence as the reference point. This creates a mirrored version of the original interval structure. Inversion was the most conceptually interesting operation for me, because it does not simply move notes around—it transforms the shape of the melody while keeping it structurally related to the original.

### Retrograde

Retrograde reverses the order of the pitch classes. If the original sequence is `[0, 2, 4, 7]`, the retrograde is `[7, 4, 2, 0]`. This is computationally the simplest operation, but musically it can have a strong effect because it changes contour, direction, and the sense of expectation.

## How the system works

My composition system starts with a pitch class sequence entered by the user in the interface. The user can also change parameters like tempo, the number of transformation steps, and the base MIDI note used for playback. Once the piece is generated, the program repeatedly chooses one of the three transformations at random and applies it to the current sequence. Each new version of the sequence contributes notes to the growing composition.

The overall process looks like this:

1. Read the user’s initial pitch class sequence.
2. Store it as the current musical material.
3. Randomly choose a transformation: transpose, inverse, or retrograde.
4. Apply that transformation to the current sequence.
5. Convert the transformed pitch classes into MIDI notes.
6. Assign durations and dynamics.
7. Append those notes to the final composition.
8. Repeat for a fixed number of steps.
9. Play the note sequence back using Web Audio.

This design gives the program both continuity and variation. Because each step begins from the previously transformed material, the composition evolves over time rather than just generating unrelated fragments.

## Mapping pitch classes to sound

After generating pitch class sequences, I needed a way to turn them into actual audible notes. To do that, I mapped each pitch class to a MIDI pitch relative to a user-defined base note. For example, if the base note is MIDI 60 (middle C), then pitch class 0 becomes 60, pitch class 4 becomes 64, and so on.

I then converted the MIDI values into frequencies and used the **Web Audio API** to synthesize tones in the browser. I used a basic oscillator-based design, which was enough for this lab because the focus was on the composition process rather than on complex synthesis. Even with simple waveforms, the system was effective because the interest came from the changing note relationships and the pacing of the generated material.

I also added slight rhythmic variation so that every note would not have exactly the same duration. This made the playback feel less mechanical and helped the output sound more like a real generated phrase rather than a rigid sequence of identical tones.

## Interface and visualization

One of the assignment requirements for pitch set theory was that the user should be able to change some aspect of the composition from the interface. I satisfied this by letting the user edit the initial pitch class sequence directly. I also added controls for:

- tempo,
- base MIDI note,
- and the number of transformation steps.

In addition to audio playback, I added a simple visualization. The program displays both the **transformation history** and a **piano-roll-style drawing** of the resulting notes. The transformation history shows how the sequence changes over time, which makes the generative process much easier to follow. The piano-roll display gives a rough visual sense of melodic contour and density.

## What I learned from implementing it myself

One of the biggest insights I gained from this lab is that automated composition does not require a huge or highly complicated system in order to produce musically meaningful results. Before writing the code, it was easy to think of algorithmic composition as something that needs advanced machine learning or very elaborate procedural logic. But building this project showed me that even a small set of carefully chosen rules can generate output that feels coherent and intentional.

Programming the transformations myself also deepened my understanding of the theory. On slides or in discussion, transpose, inverse, and retrograde can seem like abstract operations. But once I had to define them precisely in code, I understood them much more concretely. In particular, inversion became clearer when I saw how a mirrored interval structure translates into actual note values.

Another important thing I learned is that the difference between an interesting system and an uninteresting one is often not the complexity of the algorithm, but the quality of the constraints. If the system has no structure, the output tends to feel arbitrary. If the system is too rigid, the output becomes predictable. Pitch set theory works well because it balances these two extremes as the transformations preserve identity, but the random selection of operations introduces enough variation to keep the output fresh.

I also came away with a stronger appreciation for interface design in creative coding. As soon as I could type in a different pitch class set and hear the results immediately, the project stopped feeling like a homework implementation and started feeling more like a compositional instrument. That was one of the most satisfying parts of the lab.


I added a few extra features. I displayed the transformation history step by step, so the user can see the exact sequence of operations that generated the piece. I then added rhythmic variation to make the playback more expressive. I also included a simple visual representation of the generated notes over time.

In a generative system, it is easy for the output to feel mysterious in a way that is not actually helpful. Showing the process gave the piece more transparency and made it easier to connect the code to the sound.

What I found most interesting is that the project sits at the boundary between analysis and creation. Pitch set theory is often presented as a way of describing music, but in this lab I used it as a way of generating music. That shift in perspective made the material feel much more alive. Instead of just identifying transformations in an existing piece, I was using transformations to produce something new.

In the end, the lab showed me that automated composition is not just about getting a computer to make notes. It is about designing systems where musical structure can emerge from code. That was the most valuable lesson I took away from building this project.
