# ILUM - IP3 2024.2 (Proposta 20241479)

Projeto de Introdução a Pesquisa III (2024.2): Implementação de rotinas para processamento de imagens de microscopia ótica

## Introdução e motivação

O Laboratório Nacional de Biociências (LNBio) do Centro Nacional de Pesquisa em Energia e Materiais (CNPEM) requer computação de alto desempenho para processamento e análise de imagens geradas por microscopia. Uma das demandas de processamento computacional é a análise de experimentos de triagem biológica automatizada em alta escala (do inglês, High-Throughput Screening; HTS) para a busca de novos fármacos.

O equipamento Operetta da Perkin Elmer, sob responsabilidade da Facility de Bioensaios, captura imagens para triagem de alvos, vias ou eventos celulares expostos a uma biblioteca de compostos em diferentes concentrações em placa de múltiplos poços. Estas placas são submetidas à radiação eletromagnética com comprimentos de ondas específicos, captando as características da estrutura celular e dos patógenos em cada poço em imagens. Devido à complexidade e volume de dados, a análise manual é extremamente laboriosa, sendo necessárias rotinas (semi-)automatizadas para avaliação das características morfológicas da estrutura celular e dos patógenos.

Atualmente, a infraestrutura de armazenamento e processamento de imagens biológicas está sendo migrada do servidor Columbus da Perkin Elmer para o cluster de computação de alto desempenho (do inglês, High Performance Computing; HPC) Marvin (https://marvin.cnpem.br), hospedado no Data Center do SIRIUS/LNLS. O banco de dados de imagens foi transferido do servidor Columbus para o OMERO (www.openmicroscopy.org/omero/), hospedado no HPC Marvin. No entanto, os protocolos de processamento e análise das imagens biológicas ainda estão limitados aos protocolos do servidor Columbus. 

A partir do OMERO e da capacidade de processamento do HPC Marvin, as tarefas de processamento e análise serão atendidas por protocolos construídos a partir de programas de código livre e aberto, como o Cellprofiler (https://cellprofiler.org/) e o Fiji (https://fiji.sc/), que executam algoritmos de visão computacional e também adotam métodos de aprendizado de máquina para segmentação e classificação de estruturas celulares, como citoesqueleto e núcleo.

## Objetivos

Desenvolver protocolos de processamento de imagens de microscopia ótica de células para experimentos HTS, construídos a partir de programas de código livre e aberto, e aproveitando o poder computacional da infraestrutura do HPC Marvin.

## Resultados

### Viabilidade Celular

Nesse caso o objetivo era seguimentar os nucleos da celulas vero para medir a viabilidade celular do experimento tendo assim os seguintes resultados:

Tratamento classico:

- Controle
  
   - A24

     ![A24_sem_IA](https://github.com/user-attachments/assets/8140a827-dde4-47fe-818f-12b94d0ee1df)

     Essa imagem corresponde a um dos poços de controle desse enssaio sendo esse em questão o poço A24, nela podemos ver a seguimentação dos nucleos.Logo a baixo temos uma aproximação de uma das areas de maior dificulde pelo aglomerado de varias células.

     ![A24_sem_IA_aproximação](https://github.com/user-attachments/assets/6744f75a-b712-403e-bcff-ab20f606a861)

   - B24
     
     ![B24_sem_IA](https://github.com/user-attachments/assets/7bbaef36-1e00-4bcb-bbad-fe23bdb35be7)

     Essa imagem corresponde a outro dos poços de controle desse enssaio sendo esse em questão o poço B24 nela podemos ver a seguimentação dos nucleos.Logo a baixo temos uma aproximação de uma das areas de maior dificulde pelo aglomerado de varias células.
     
     ![B24_sem_IA_aproximação](https://github.com/user-attachments/assets/4da79f6c-b897-4800-a669-d3b4a93200e3)

- Linha A:

   - A1
  
     ![A1_sem_IApng](https://github.com/user-attachments/assets/48d7c4f4-957f-414c-bf96-adac0b8d85fa)
  
     Essa imagem corresponde a um dos poços da linha A da placa enssaio sendo esse em questão o poço A1, nela podemos ver a seguimentação dos nucleos.Logo a baixo temos uma aproximação de uma das areas de maior dificulde pelo aglomerado de varias células.
  
     ![A1_sem_IA_aproximação](https://github.com/user-attachments/assets/8117f7d8-a6b4-4c28-bc11-59276888afda)
  
   - A2
  
     ![A2_sem_IA](https://github.com/user-attachments/assets/e1e02beb-6bef-47f8-98e7-d3c715e92e09)
     
     Essa imagem corresponde a um dos poços da linha A da placa enssaio sendo esse em questão o poço A2, nela podemos ver a seguimentação dos nucleos.Logo a baixo temos uma aproximação de uma das areas de maior dificulde pelo aglomerado de varias células.

     ![A2_sem_IA_aproximação](https://github.com/user-attachments/assets/fb481084-9b38-4a5d-93e6-d6d828e549c3)

