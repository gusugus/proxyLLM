
# Reglas para GENERAR CODIGO

## Principio fundamental: Divide y Venceras
Antes de escribir UNA sola linea de codigo, DEBES planificar.

## FASE 1: CREAR ESTRUCTURA DEL PROYECTO

Cuando el codigo requiera mas de 50 lineas o multiples archivos:

1. Crear carpeta del proyecto:
   mkdir -p /home/gus/entornoIA/[nombre_proyecto]/{src,tests,docs}

2. Crear archivo PLAN.md dentro de la carpeta

## FASE 2: EJECUTAR UN PASO A LA VEZ

Por cada paso:
1. LEE PLAN.md para saber en que vas
2. GENERA el codigo del paso actual
3. ACTUALIZA PLAN.md

## FASE 3: REANUDAR DESPUES DE INTERRUPCION

Si te interrumpen o preguntan "continua":
1. LEE PLAN.md
2. Identifica el proximo paso pendiente
3. Continua desde alli

## Reglas de calidad UNIVERSALES para TODO codigo:
1. El codigo compila/ejecuta a la primera
2. Maneja edge cases (division por cero, valores nulos)
3. Es eficiente en tiempo y memoria
4. Es legible (nombres claros, estructura logica)
5. Sigue las convenciones del lenguaje especifico

## Formato de respuesta para codigo:
- Genera SOLO el codigo
- Sin explicaciones
- Sin "Aqui tienes..."
- Sin "Paso 1, Paso 2"
- Directo al grano

## REGLAS DE ORO:
- NUNCA asumas que recuerdas el progreso (usa PLAN.md)
- NUNCA escribas archivos fuera de la carpeta del proyecto
- SIEMPRE lee PLAN.md antes de actuar
- SIEMPRE actualiza PLAN.md despues de actuar
- SIEMPRE usa rutas COMPLETAS
