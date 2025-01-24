# Open Science Toolkit for Information Access (OSTIA)

![CI](https://github.com/adrianrome/OSTIA/actions/workflows/main.yaml/badge.svg)
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![MIT License][license-shield]][license-url]

## About the Project

The **Open Science Toolkit for Information Access (OSTIA)** is an open-source tool designed to process and visualize access data from repositories like UPCommons, the open-access platform of the Universitat Politècnica de Catalunya. This project integrates advanced data processing techniques to derive valuable insights from logs generated between 2006 and 2023, comprising a dataset of over 1.9 billion records.

Key features include:
- **Log Processing**: Advanced filtering to remove bots, duplicates, and irrelevant records while adhering to COUNTER metrics.
- **Data Enrichment**: Integration of metadata, such as authorship, licensing, and resource type, for comprehensive insights.
- **Visualization**: Seamless integration with Grafana for dynamic dashboards and reports.

## Project Structure

<pre>
.
├── LICENSE
├── Pipfile
├── Makefile
├── README.md
├── requirements.txt
├── .pre-commit-config.yaml
├── .github/
│   └── workflows/
├── config/
│   ├── loki/
│   ├── mongo/
│   └── nginx/
│       └── certificates/
├── docs/
│   └── source/
├── src/
│   ├── dashboards/
│   ├── logs/
│   │   ├── counter/
│   │   ├── filter/
│   │   ├── forwarder/
│   │   ├── transformer/
│   │   └── utils/
│   └── metadata/
│       ├── filter/
│       ├── forwarder/
│       ├── oaipmh/
│       ├── parser/
│       └── utils/
└── test/
    ├── logs/
    └── metadata/
</pre>

## Built With

[![Bash][bash]][bash-url]
[![Docker][docker]][docker-url]
[![Git][git]][git-url]
[![GitHub Actions][github-actions]][github-actions-url]
[![GitHub][github]][github-url]
[![Grafana][grafana]][grafana-url]
[![MongoDB][mongodb]][mongodb-url]
[![Nginx][nginx]][nginx-url]
[![Python][python]][python-url]

## License

This project is distributed under the MIT License. See `LICENSE` for more details.

## Contact

[![LinkedIn][linkedin-shield]][linkedin-url]
[![e-mail][email-shield]][email-url]
Adrián Romera González

[bash]: https://img.shields.io/badge/GNU%20Bash-4EAA25?logo=gnubash&logoColor=fff&style=for-the-badge
[bash-url]: https://www.linuxfoundation.org/
[contributors-shield]: https://img.shields.io/github/contributors/adrianrome/OSTIA.svg?style=flat
[contributors-url]: https://github.com/adrianrome/OSTIA/graphs/contributors
[docker]: https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff&style=for-the-badge
[docker-url]: https://www.docker.com/
[email-shield]:https://img.shields.io/badge/contact-email-blue
[email-url]: mailto:aromerag@outlook.com
[forks-shield]: https://img.shields.io/github/forks/adrianrome/OSTIA.svg?style=flat
[forks-url]: https://github.com/adrianrome/OSTIA/network/members
[git]: https://img.shields.io/badge/Git-F05032?logo=git&logoColor=fff&style=for-the-badge
[github]: https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=fff&style=for-the-badge
[github-actions]: https://img.shields.io/badge/GitHub%20Actions-2088FF?logo=githubactions&logoColor=fff&style=for-the-badge
[github-actions-url]: https://github.com/features/actions
[github-url]: https://github.com/
[git-url]: https://git-scm.com/
[grafana]: https://img.shields.io/badge/Grafana-F46800?logo=grafana&logoColor=fff&style=for-the-badge
[grafana-url]: https://grafana.com/
[license-shield]: https://img.shields.io/github/license/adrianrome/OSTIA.svg?style=flat
[license-url]: https://github.com/adrianrome/OSTIA/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/aromerag/
[mongodb]: https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=fff&style=for-the-badge
[mongodb-url]: https://www.mongodb.com/
[nginx]: https://img.shields.io/badge/NGINX-009639?logo=nginx&logoColor=fff&style=for-the-badge
[nginx-url]: https://nginx.org/
[python]: https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge
[python-url]: https://www.python.org/
[stars-shield]: https://img.shields.io/github/stars/adrianrome/OSTIA.svg?style=flat
[stars-url]: https://github.com/adrianrome/OSTIA/stargazers
