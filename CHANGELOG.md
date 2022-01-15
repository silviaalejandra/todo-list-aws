# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2021-01-08
### Added
- Versión inicial de código. Nueva version

## [1.0.1] - 2022-01-13
- Se crea rama feature para inicio de despliegue version local
- Se actualizan los bucket en el archivo samconfig.toml
- Se actualiza README con pasos realizados para levantar entorno local
- 
## [1.0.2] - 2022-01-14
- Se crear Jenkinsfile parametrizable para ejecucion de staging y production
- Se cambian los nombres de los directorios PIPELINE-FULL-STAGING y PIPELINE-FULL-PRODUCTION por PIPELINE-FULL-staging PIPELINE-FULL-production para poder realizar la parametría del pipeline multibranch
- Se actualiza README con los cambios en la configuracion del pipeline para ejecucion full staging o full production
- Se agrega log de deply manual realizado desde consola (logs/deployManual.log)
- 
## [1.0.3] - 2022-01-15
- Se agregan los logs de jenkins del despliegue en staging
- Se agregar los logs de jenkins del despliegue de production