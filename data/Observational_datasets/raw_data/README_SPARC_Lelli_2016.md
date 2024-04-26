## Dataset Description


| Units | Label         | Explanations                       |
|-------|---------------|------------------------------------|
| ---   | Galaxy        | Galaxy Name                        |
| Msun  | M*            | Stellar Mass                       |
| kpc   | Reff          | Effective Radius at [3.6]          |
| ---   | fDM(Reff)     | Dark Matter Fraction within Reff   |
| ---   | Errorfdm(Reff)| Error on fDM(Reff)                 |
| ---   | Q             | Quality Flag (1 = High, 2 = Medium, 3 = Low)


### SPARC 
Data from the SPARC dataset ([SPARC](http://astroweb.cwru.edu/SPARC/)):
> SPARC is a database of 175 late-type galaxies (spirals and irregulars) with Spitzer photometry at 3.6 µm (tracing the stellar mass distribution) and high-quality HI+Hα rotation curves (tracing the gravitational potential out to large radii). SPARC spans a wide range in stellar masses (5 dex), surface brightnesses (>3 dex), and gas fractions.

For more, check the main paper "[SPARC](http://astroweb.cwru.edu/SPARC/)".
The following quantities are extracted from the dataset:

- <span style="background-color: lightgray">fDM</span>: This represents the dark matter fraction.
- <span style="background-color: lightgray">ErrorfDM</span>: This represents the uncertainty on the dark matter fraction.
- <span style="background-color: lightgray">Reff</span>: Effective radius [kpc].


For our analysis, we employ a constant mass-to-light ratio of $\Gamma = 0.5 M⊙/L⊙$, as determined by stellar population synthesis models (Schombert & McGaugh 2014) based on a Chabrier IMF. Following Lelli et al. (2016) and utilizing their rotation curve calculations, we compute the fraction of dark matter using, with $\Gamma_{bul} = 1.4\Gamma_{disk}$ and $\Gamma_{disk} = 0.5$ : 

$$V_{bar}^2 = V_{gas}|V_{gas}| + \Gamma_{disk}V_{disk}|V_{disk}| + \Gamma_{bul}V_{bul}|V_{bul}|$$

$$f_{DM} = \frac{{V_{obs}^2 - V_{bar}^2}}{{V_{obs}^2}}$$
