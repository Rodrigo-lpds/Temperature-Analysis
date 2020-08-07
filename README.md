# Criação de projeções de Temperatura em Topo de Nuvem

## Descrição
O projeto foi criado com o objetivo de utilizar dados geoespaciais (de formato **NetCDF**) dados pelo satélite **GOES-16** para confecção de projeções. A partir dos **16** canais do satélite podemos extrair diferentes tipos de dados, sendo cada canal diferente entre si por estarem em frequencias diferentes.
Neste projeto, o canal **13** foi escolhido, pois mostrou-se ser o ideal para criação de projeções que determinem a temperatura em topo de nuvem.

## Instalação
Para a execução dos scripts que serão mencionados posteriormente, será necessária a instalação de certos programas.

#### Anaconda
Distribuição que nos dará as ferramentas necessárias para uma execução mais prática e direta.
O download da distribuição pode ser encontrado no [site oficial](https://www.anaconda.com), e até o momento por este [link](https://www.anaconda.com/distribution/#download-section).

**Importante: É recomendado que após a instalação completa do Anaconda, seja criado um Ambiente, ou Environment, _específico_ para o projeto.**
#### Spyder
IDE que utilizaremos para plotar as projeções e para debugar os scripts.
As instruções para download podem ser encontradas neste [link](https://docs.spyder-ide.org/installation.html).

Agora será necessário a instalação de pacotes pelo Anaconda. Abra o **Anaconda Prompt** e digite estes comandos no terminal:

Biblioteca para Python e suas dependencias, necessárias para manipulação de dados **NetCDF's**. Para mais informações [acesse](https://anaconda.org/anaconda/netcdf4).
> conda install -c conda-forge netCDF4

Biblioteca **matplotlib basemap** responsável por plotar dados 2D de mapas em Python. Para mais informações [acesse](https://matplotlib.org/basemap/index.html).
> conda install -c conda-forge basemap

Biblioteca parecida com a **PIL**, responsável por auxiliar no processamento de imagens pelo interpretador Python. 
> conda install -c anaconda pillow 

Biblioteca **GDAL** responsável por manipular dados GeoEspaciais
> conda install -c conda-forge gdal


## Agora que todo o ambiente está configurado, execute o Tutorial_Rj.py e assim deve obter esta projeção abaixo:

![RJ_G16_C13_28-Oct-2019_08_40_38](https://user-images.githubusercontent.com/56642493/89683869-b5507400-d8cf-11ea-8fdc-8f8b780b53c3.png)



## Créditos
Script criado por mim: Rodrigo Lucas Pinto da Silva. [Github](https://github.com/Rodrigo-lpds) e [Linkedin](https://www.linkedin.com/in/rodrigo-lucas-pinto-da-silva-3684a8179/)

Usando como referencia o blog: [GEONETClass - Americas](https://geonetcast.wordpress.com) e seus tutoriais incriveis que podem ser [encontrados aqui](https://geonetcast.wordpress.com/gnc-a-product-manipulation-tutorials/).

E mentoria teórica de **Meteorologia e Dados Via Satélite** por [Fabio Hochleitner](https://www.linkedin.com/in/fabioh/) 
