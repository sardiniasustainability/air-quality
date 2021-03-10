industrialCombustion = readtable('data/industrial-combustion-processes-2010.csv');
industrialCombustion.Inquinante = string(industrialCombustion.Inquinante);
%%
pollutants = unique(industrialCombustion.Inquinante);
currPollutant = pollutants(18);
currData = industrialCombustion(industrialCombustion.Inquinante==currPollutant, :);
map = shaperead('geo/comune-limits.shp');
% plotMap = outerjoin(map, currData, 'LeftKeys', 'nome', 'RightKeys', 'Comune', 'RightVariables', 'Valore');
% head(plotMap)

mapFigure = figure();
mapAxes = axes(mapFigure);

faceColorSpec = cell(1, height(currData)+1);
minVal = min(currData.Valore);
maxVal = max(currData.Valore);
numLevels = 32;
colorMap = parula(numLevels);
for k = 1:height(currData)
    currColLevel = 1+round(...
        (numLevels-1)*...
        ((currData.Valore(k)-minVal)/(maxVal-minVal)));
    faceColorSpec{k} = {'nome', currData.Comune{k}, 'FaceColor', colorMap(currColLevel, :)};
end
faceColorSpec{end} = {'Default', 'FaceColor', 'w'};
colorRange = makesymbolspec('Polygon', faceColorSpec{:});
plot = mapshow(map, 'DisplayType', 'Polygon', 'SymbolSpec', colorRange);
ax = plot.Parent;
ax.Visible = 'off';
title(ax, currPollutant);
ax.YLim(2) = ax.YLim(1)+((ax.YLim(2)-ax.YLim(1))/2);

tickLabels = string(minVal:maxVal);
ticks = linspace(0, 1, numel(tickLabels));
sideBar = colorbar(ax, "eastoutside", 'Ticks', ticks, 'TickLabels', tickLabels);
%%
x = readtable('data/sarroch-co-2020.csv');
head(x)