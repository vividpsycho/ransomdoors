using NAudio.Wave;
using System.IO;

namespace rans0m
{
    /// <summary>
    /// Random JX1DX1 voice lines and their exact captions from the FORSAKEN wiki.
    /// Audio files are embedded under Assets/Sounds/Noli by the repository fetch workflow.
    /// </summary>
    internal static class NoliVoiceLines
    {
        private sealed record VoiceLine(string File, string Caption);

        private static readonly VoiceLine[] Lines =
        {
            new("JX1DX1Intro1.mp3", "JUST.HOW.REAL.AM.I"),
            new("JX1DX1IntroUnused.mp3", "YOU.ARE.ALL.NOTHING.BUT.SHEEP.TO.ME"),
            new("JX1DX1Intro2.mp3", "BYSTANDER.NO.LONGER"),
            new("JX1DX1Outro.mp3", "GORGEOUS.IS.IT.NOT"),
            new("JX1DX1VoidRushStartup1.mp3", "WATCH.YOUR.SIX"),
            new("JX1DX1VoidRushStartup2.mp3", "BE READY"),
            new("JX1DX1VoidRushStartup3.mp3", "DO.NOT.BLINK"),
            new("JX1DX1VoidRushSlam1.mp3", "YOU.ARE.NOT.PERCEPTIVE"),
            new("JX1DX1VoidRushSlam2.mp3", "ONE.WITH.THE.PAVEMENT"),
            new("JX1DX1VoidRushCrash.mp3", "[LAUGHTER]"),
            new("JX1DX1Nova1.mp3", "TICK.TOCK"),
            new("JX1DX1Nova2.mp3", "TARGET.MARKED"),
            new("JX1DX1Nova3.mp3", "STAY STILL, WILL YOU"),
            new("JX1DX1ObservantStartup1.mp3", "BIG.BROTHER.IS.WATCHING"),
            new("JX1DX1ObservantStartup2.mp3", "MY.MANY.EYES"),
            new("JX1DX1ObservantTeleport1.mp3", "PEEK.A.BOO"),
            new("JX1DX1ObservantTeleport2.mp3", "SCRIPT.INJECTED"),
            new("JX1DX1Hallucination.mp3", "[LAUGHTER]"),
            new("JX1DX1Stun1.mp3", "I.CAN.SEE.YOU.BEHIND.THAT.SCREEN"),
            new("JX1DX1Stun2.mp3", "ONLY.A.SETBACK"),
            new("JX1DX1Stun3.mp3", "RELISH.THE.FEEL.OF.YOUR.BREATH"),
            new("JX1DX1Stun4.mp3", "IT.IS.A.MATTER.OF.TIME"),
            new("JX1DX1Kill1.mp3", "A.TASTE.OF.NILSPACE"),
            new("JX1DX1Kill2.mp3", "A.BIT.OF.AGONY.TO.SPARE"),
            new("JX1DX1Kill3.mp3", "BARELY.AN.OBSTACLE"),
            new("JX1DX1Kill4.mp3", "PURGED.FROM.HISTORY"),
            new("JX1DX1Kill5.mp3", "NO.SOUND.NO.MEMORY"),
            new("JX1DX1Kill6.mp3", "TELL.NIKO.I.SENT.YOU"),
            new("JX1DX1Kill007n7.mp3", "REMOVING.DATA.MODEL"),
            new("JX1DX1KillDeivy.mp3", "NOTHING.MORE.THAN.COUNTERFEIT"),
            new("JX1DX1KillBuliderman.mp3", "THE.INTERFACE.YOU.CREATED"),
            new("JX1DX1KillDragondude3.mp3", "ARE.THE.STARS.NOT.BEAUTIFUL"),
            new("JX1DX1KillFOTL.mp3", "ANTHRACITE.CHARS.YOUR.HEART.JACK"),
            new("JX1DX1KillAubree1.mp3", "THIS.IS.NOT.A.DAYCARE"),
            new("JX1DX1KillAubree2.mp3", "SHE.WOULD.NOT.BE.PROUD"),
            new("JX1DX1KillAubree3.mp3", "DO.SAY.HI.TO.HER.FOR.ME"),
            new("JX1DX1KillAubree4.mp3", "YOU.WILL.NEVER.FIND.PEACE"),
            new("JX1DX1KillSpiders.mp3", "THIS.IS.NOT.A.DAYCARE"),
            new("JX1DX1LMS1.mp3", "YOU.ARE.A.BAD.LISTENER"),
            new("JX1DX1LMS2.mp3", "WHAT.A.FAILURE"),
            new("JX1DX1LMS3.mp3", "IS.THIS.REAL.ENOUGH.FOR.YOU"),
            new("JX1DX1LMSDeivy.mp3", "THANK.YOU.FOR.BEING.A.GOOD.EXAMPLE"),
            new("JX1DX1LMSDragondude3.mp3", "LOOK.AT.ALL.THE.LONELY.PEOPLE"),
            new("JX1DX1LMSFOTL.mp3", "DO.YOU.STILL.WISH.THAT.YOUR.FRIENDS.FOLLOWED"),
            new("JX1DX1LMSAubree.mp3", "SITTING.BACK.ROTTING.LIKE.ALWAYS"),
            new("JX1DX1No1.mp3", "I.THINK.NOT"),
            new("JX1DX1No2.mp3", "WHAT.NARROW.INSIGHT"),
            new("JX1DX1Yes1.mp3", "AND.PATIENTLY.I.WILL.WAIT.FURTHER"),
            new("JX1DX1Yes2.mp3", "ALL.IN.DUE.TIME"),
            new("JX1DX1Taunt1.mp3", "I.CAN.HEAR.YOU"),
            new("JX1DX1Taunt2.mp3", "YOUR.ACUMEN.IS.LACKING"),
            new("JX1DX1Rage1.mp3", "STOP.WORRYING"),
            new("JX1DX1Rage2.mp3", "THE.CLOCK.IS.TICKING"),
            new("JX1DX1Laugh1.mp3", "[LAUGHTER]"),
            new("JX1DX1IdleUnused1.mp3", "PERHAPS.YOU.WILL.BE.NEXT.PLAYER"),
            new("JX1DX1IdleUnused2.mp3", "YOU.ARE.HEARTLESS.WE.WILL.GET.ALONG.FINE")
        };

        public static bool TryPlayRandom(Window window)
        {
            if (Lines.Length == 0) return false;

            // Try several entries so a missing/unavailable asset does not prevent a taunt.
            foreach (int index in Enumerable.Range(0, Lines.Length).OrderBy(_ => Global.rng.Next()).Take(Lines.Length))
            {
                VoiceLine line = Lines[index];
                try
                {
                    Stream stream = Global.GetResourceSteam("Sounds/Noli/" + line.File);
                    var reader = new Mp3FileReader(stream);
                    var output = new WaveOutEvent();
                    output.Init(reader);
                    output.PlaybackStopped += (_, _) =>
                    {
                        output.Dispose();
                        reader.Dispose();
                    };
                    window.Title = line.Caption;
                    output.Play();
                    return true;
                }
                catch
                {
                    // This voice line has not been downloaded/embedded yet; try another.
                }
            }

            return false;
        }
    }
}
