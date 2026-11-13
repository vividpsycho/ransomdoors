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
            "pack://application:,,,/Assets/Taunts/jx1dx1.gif"
        };

        public TauntWindow()
        {
            InitializeComponent();
            Closed += (_, _) => _closed = true;
        }

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            Global.HideSystemMenu(this);

            // Every taunt gets an independently randomized title, visual, size and lifetime.
            Title = "JX1DX1";
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

            Close();
        }
    }
}