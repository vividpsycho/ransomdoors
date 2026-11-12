using System;
using System.IO;
using System.Windows;
using System.Windows.Media;
using XamlAnimatedGif;

namespace rans0m
{
    public partial class TauntWindow : Window
    {
        private bool _closed;

        private static readonly string[] AnimatedTaunts =
        {
            "pack://application:,,,/Assets/static.gif",
            "pack://application:,,,/Assets/ransom_attack.gif",
            "pack://application:,,,/Assets/red_vignette.gif",
            "pack://application:,,,/Assets/repent.gif"
        };

        public TauntWindow()
        {
            InitializeComponent();
            Closed += (_, _) => _closed = true;
        }

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            Global.HideSystemMenu(this);

            try
            {
                Stream tauntSpawnStream = Global.GetResourceSteam("Sounds/tauntSpawn.wav");
                _ = Task.Run(() => SoundHandle.Create(tauntSpawnStream).Play());
            }
            catch { }

            // Every taunt gets an independently randomized title, visual, size and lifetime.
            Title = Global.tauntTitles[Global.rng.Next(Global.tauntTitles.Count)];
            NoliVoiceLines.TryPlayRandom(this);

            bool useAnimation = Global.rng.Next(100) < 55;
            if (useAnimation)
            {
                string source = AnimatedTaunts[Global.rng.Next(AnimatedTaunts.Length)];
                AnimationBehavior.SetSourceUri(tauntImage, new Uri(source));
                tauntImage.Stretch = Global.rng.Next(2) == 0
                    ? Stretch.UniformToFill
                    : Stretch.Fill;
            }
            else
            {
                Background = new ImageBrush(Global.tauntImages[Global.rng.Next(Global.tauntImages.Count)])
                {
                    Stretch = Global.rng.Next(2) == 0 ? Stretch.UniformToFill : Stretch.Fill
                };
                tauntImage.Visibility = Visibility.Collapsed;
            }

            Width = Global.rng.Next(190, 461);
            Height = Global.rng.Next(190, 461);
            Opacity = Global.rng.Next(82, 101) / 100.0;

            Global.RandomPosWindow(this);
            Global.GlitchIdle(this);
            _ = CloseAfterDelayAsync();
        }

        private async Task CloseAfterDelayAsync()
        {
            await Task.Delay(Global.rng.Next(3500, 10001));
            if (_closed) return;

            try { SoundHandle.Create(Global.GetResourceSteam("Sounds/tauntLeave.wav")).Play(); }
            catch { }

            Close();
        }
    }
}